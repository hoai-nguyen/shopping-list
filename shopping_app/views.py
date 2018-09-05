from flask import request, jsonify
from shopping_app import app, helpers


@app.route('/shopping_list', methods=['POST'])
def add_shopping_list():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.add_shopping_list(request.json)


@app.route('/item', methods=['POST'])
def add_item():
    if not request.json:
        jsonify({"message": "Require body."}), 400

    return helpers.add_item(request.json)

