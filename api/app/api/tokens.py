from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import unauthorized
from app.models import Role, User
from flask import jsonify


@bp.route("/tokens", methods=["POST"])
@basic_auth.login_required
def get_token():
    """Initial entrypoint of any user of the application. Only time basic auth
    (username:password) is used. The user afterward should get their token and
    store it in a cookie for example."""
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({"token": token})


@bp.route("/tokens/<int:id>", methods=["DELETE"])
@token_auth.login_required
def revoke_token(id):
    """Allows a user to revoke their token or an admin to revoke
    the token of any user."""
    current_is_reuf_admin = token_auth.current_user().has_one_of_roles(
        [Role.REUF_ADMIN]
    )
    if token_auth.current_user().id != id and not current_is_reuf_admin:
        return unauthorized()
    user = User.query.get_or_404(id)
    user.revoke_token()
    db.session.commit()
    return "", 204


@bp.route("/tokens/", methods=["DELETE"])
@token_auth.login_required(role=[Role.REUF_ADMIN])
def revoke_all_token():
    """Allows an admin to revoke the tokens of every users. They should all
    re-authenticate with basic auth to obtain a new one."""
    all_users = User.query.all()
    [u.revoke_token() for u in all_users]
    db.session.commit()
    return "", 204
