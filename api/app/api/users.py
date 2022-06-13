from flask import jsonify, request, url_for, abort
from app import db
from app.models import User, Role
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route("/users/<int:id>", methods=["GET"])
@token_auth.login_required(role=[Role.REUF_ADMIN, Role.REUF])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route("/users", methods=["GET"])
@token_auth.login_required(role=[Role.REUF_ADMIN, Role.REUF])
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, "api.get_users")
    return jsonify(data)


@bp.route("/users", methods=["POST"])
def create_user():
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
    if (
        token_auth.current_user().id != id
        and not token_auth.current_user().is_reuf_admin
    ):
        abort(403)
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
    if (
        "role" in data
        and [Role(r) for r in data["role"]] != token_auth.get_user_roles(user)
        and not Role.REUF_ADMIN in token_auth.get_user_roles(token_auth.current_user())
    ):
        return bad_request("please contact an admin for changing your admin status")
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
