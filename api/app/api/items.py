from flask import jsonify
from app.api import bp
from app.api.auth import token_auth


@bp.route("/get_item/<int:id>", methods=["GET"])
@token_auth.login_required
def get_item(id):
    return jsonify({})


@bp.route("/get_item_image/<int:id>", methods=["GET"])
@token_auth.login_required
def get_item_image(id):
    return jsonify({})


@bp.route("/update_item/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_item(id):
    return jsonify({})