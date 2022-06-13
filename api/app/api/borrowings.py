from flask import jsonify
from app.api import bp
from app.api.auth import token_auth


@bp.route("/get_borrowings_with_item/<int:id>", methods=["GET"])
@token_auth.login_required
def get_borrowings_with_item(id):
    return jsonify({})


@bp.route("/get_borrowings_for_user/<int:id>", methods=["GET"])
@token_auth.login_required
def get_borrowings_for_user(id):
    return jsonify({})


@bp.route("/get_borrowings/", methods=["GET"])
@token_auth.login_required
def get_borrowings():
    return jsonify({})

@bp.route("/borrow_item/<int:id>", methods=["GET"])
@token_auth.login_required
def borrow_item(id):
    return jsonify({})