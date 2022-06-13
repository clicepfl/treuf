from app import db
from app.errors import bp
from app import email
from app.api.errors import error_response as api_error_response


@bp.app_errorhandler(403)
def forbidden_error(error):
    return api_error_response(403)


@bp.app_errorhandler(404)
def not_found_error(error):
    return api_error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return api_error_response(500)
