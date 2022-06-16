from flask import jsonify
from app.api import bp
from app.api.auth import token_auth
from app.models import Role, Item


@bp.route("/items/<int:id>", methods=["GET"])
@token_auth.login_required
def get_item(id):
    return jsonify({})


@bp.route("/items/", methods=["GET"])
@token_auth.login_required
def get_items():
    return jsonify({})


@bp.route("items/image/<int:id>", methods=["GET"])
@token_auth.login_required
def get_item_image(id):
    return jsonify({})


@bp.route("/items/", methods=["POST"])
@token_auth.login_required(role=[Role.REUF, Role.REUF_ADMIN])
def add_item():
    return jsonify({})


@bp.route("items/image/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_item_image(id):
    return jsonify({})


@bp.route("/items/<int:id>", methods=["PUT"])
@token_auth.login_required
def update_item(id):
    return jsonify({})


@bp.route("/items/<int:id>", methods=["DELETE"])
@token_auth.login_required(role=[Role.REUF, Role.REUF_ADMIN])
def delete_item():
    return jsonify({})
