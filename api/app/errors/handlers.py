from app import db
from app.errors import bp
from app import email

@bp.app_errorhandler(404)
def not_found_error(error):
    return "", 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "", 500