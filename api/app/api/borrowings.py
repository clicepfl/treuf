from flask import jsonify
from app.api import bp
from app.api.auth import token_auth


@bp.route("/borrowings/with_item/<int:id>", methods=["GET"])
@token_auth.login_required
def get_borrowings_with_item(id):
    return jsonify({})


@bp.route("/borrowings/for_user/<int:id>", methods=["GET"])
@token_auth.login_required
def get_borrowings_for_user(id):
    return jsonify({})


@bp.route("/borrowings/<int:id>", methods=["GET"])
@token_auth.login_required
def get_borrowing(id):
    return jsonify({})


@bp.route("/borrowings/", methods=["GET"])
@token_auth.login_required
def get_borrowings():
    return jsonify({})


@bp.route("/borrowings/<int:id>", methods=["PUT"])
@token_auth.login_required
def modify_borrowing(id):
    return jsonify({})


@bp.route("/borrowings/borrow/<int:item_id>/<int:user_id>", methods=["POST"])
@token_auth.login_required
def borrow_item(item_id, user_id):
    return jsonify({})


@bp.route("/borrowings/<int:id>", methods=["DELETE"])
@token_auth.login_required
def delete_borrowing(id):
    return jsonify({})
