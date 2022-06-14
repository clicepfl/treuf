from flask import jsonify, request, url_for, abort
from app import db
from app.models import User, Role
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request, unauthorized


@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required()
def get_user(id):
    """Retrieves information of the user with the given id. Users can only see their informations, only reufs can see informations of other users."""
    current_is_reuf = token_auth.current_user().has_one_of_roles(
        [Role.REUF, Role.REUF_ADMIN]
    )
    if token_auth.current_user().id != id and not current_is_reuf:
        return unauthorized()
    return jsonify(User.query.get_or_404(id).to_dict(current_is_reuf))


@bp.route("/users", methods=["GET"])
@token_auth.login_required(role=[Role.REUF_ADMIN, Role.REUF])
def get_users():
    """Retrieves a paginated view of all the users. Only admins are allowed for this request.

    Args (in the GET request):
        - page: the page we want to have informations for
        - per_page: the number of elements per page. 10 by default, should be less that 100"""
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, "api.get_users")
    return jsonify(data)


@bp.route("/users", methods=["POST"])
def create_user():
    """Creates a new user from the content of the POSTed value"""
    data = request.get_json() or {}
    if (
        "username" not in data
        or "email" not in data
        or "password" not in data
        or "sciper" not in data
    ):
        return bad_request("must include username, email, password and sciper fields")
    if "role" in data:
        # we do not allow direct creation of admin/staff users. Users can only be upgraded via update by an admin user.
        return bad_request("must contact an admin to create an admin user")
    if User.query.filter_by(username=data["username"]).first():
        return bad_request("please use a different username")
    if User.query.filter_by(email=data["email"]).first():
        return bad_request("please use a different email address")
    if User.query.filter_by(sciper=data["sciper"]).first():
        return bad_request("please use a different sciper number")
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers["Location"] = url_for("api.get_user", id=user.id)
    return response


@bp.route("/users/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_user(id):
    current_is_reuf_admin = token_auth.current_user().has_one_of_roles(
        [Role.REUF_ADMIN]
    )
    if token_auth.current_user().id != id and not current_is_reuf_admin:
        return unauthorized()
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if (
        "username" in data
        and data["username"] != user.username
        and User.query.filter_by(username=data["username"]).first()
    ):
        return bad_request("please use a different username")
    if (
        "email" in data
        and data["email"] != user.email
        and User.query.filter_by(email=data["email"]).first()
    ):
        return bad_request("please use a different email address")
    if (
        "sciper" in data
        and data["sciper"] != user.sciper
        and User.query.filter_by(sciper=data["sciper"]).first()
    ):
        return bad_request("please use a different sciper number")
    if "role" in data:
        if not current_is_reuf_admin:
            return bad_request("please contact an admin for changing your admin status")
        try:
            [Role(r) for r in data["role"]]
        except ValueError:
            return bad_request("the given roles do not exist")
    user.from_dict(data, new_user="password" in data)
    db.session.commit()
    return jsonify(user.to_dict())
