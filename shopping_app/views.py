from flask import request, jsonify
from shopping_app import app, request_handlers


@app.route('/shopping_list', methods=['POST']) # TODO docs string
def add_shopping_list():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return request_handlers.add_shopping_list(request.json)


@app.route('/item', methods=['POST'])
def add_item():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return request_handlers.add_item(request.json)


@app.route('/shopping_list/<int:shopping_list_id>', methods=['PUT'])
def update_shopping_list(shopping_list_id):
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return request_handlers.update_shopping_list(shopping_list_id, request.json)


@app.route('/shopping_list/<shopping_list_id>', methods=['DELETE'])
def delete_shopping_list(shopping_list_id):

    return request_handlers.delete_shopping_list(shopping_list_id)


@app.route('/item_shopping_list', methods=['POST'])
def add_item_to_shopping_list():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return request_handlers.add_item_to_shopping_list(request.json)


@app.route('/all_shopping_lists', methods=['GET'])
def get_all_shopping_lists():

    return request_handlers.get_all_shopping_lists()


@app.route('/shopping_list/<title>', methods=['GET'])
def get_shopping_list_by_title(title):

    return request_handlers.get_shopping_list_by_title(title)


@app.route('/shopping_list_by_title_keyword/<keyword>', methods=['GET'])
def get_shopping_list_by_keyword(keyword):

    return request_handlers.get_shopping_list_by_keyword(keyword)


@app.route('/shopping_list_by_item_id/<int:item_id>', methods=['GET'])
def get_shopping_list_by_item_id(item_id):

    return request_handlers.get_shopping_list_by_item_id(item_id)


@app.route('/shopping_list_by_item_name_keyword/<keyword>', methods=['GET'])
def get_shopping_list_by_item_name_keyword(keyword):

    return request_handlers.get_shopping_list_by_item_name_keyword(keyword)