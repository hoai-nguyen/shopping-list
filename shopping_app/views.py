from flask import request, jsonify
from shopping_app import app, helpers


@app.route('/shopping_list', methods=['POST']) # TODO docs string
def add_shopping_list():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.add_shopping_list(request.json)


@app.route('/item', methods=['POST'])
def add_item():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.add_item(request.json)


@app.route('/shopping_list/<shopping_list_id>', methods=['PUT'])
def update_shopping_list(shopping_list_id):
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.update_shopping_list(shopping_list_id, request.json)


@app.route('/shopping_list/<shopping_list_id>', methods=['DELETE'])
def delete_shopping_list(shopping_list_id):

    return helpers.delete_shopping_list(shopping_list_id)


@app.route('/item_shopping_list', methods=['POST'])
def add_item_to_shopping_list():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.add_item_to_shopping_list(request.json)


