# -*- coding: utf-8 -*-

from flask import request, jsonify

from shopping_app import app, request_handlers
from shopping_app.constants import RES_REQUIRE_BODY, RES_NOT_ACCEPTABLE


@app.route('/shopping_list', methods=['POST'])
def add_shopping_list():
    """API to add new shopping list to DB.

    Method: POST
    Parameters: n/a
    Request header:
        required: Content-Type = application/json, Accept = application/json
    Request body: Request body should contain shopping list 'store_name' and 'title', for example:
        {
            "store_name": "FPT"
            , "title": "Rice"
        }
    Responses:
      500: If any exception occurs and failed to add shopping list to DB.
      400: If bad request is sent.
      200: Add shopping list to DB successfully.

    @:return API response
    """
    if not request.is_json:
        return jsonify(RES_NOT_ACCEPTABLE), 400

    if not request.data:
        return jsonify(RES_REQUIRE_BODY), 400

    return request_handlers.add_shopping_list(request.json)


@app.route('/item', methods=['POST'])
def add_item():
    """API to add new item to DB.

    Method: POST
    Parameters: n/a
    Request header:
        required: Content-Type = application/json, Accept = application/json
    Request body: Request body should contain item 'name', for example:
        {"name": "Rice"}
    Responses:
      500: If any exception occurs and failed to add item to DB.
      400: If bad request is sent.
      200: Add item to DB successfully.

    @:return API response
    """
    if not request.is_json:
        return jsonify(RES_NOT_ACCEPTABLE), 400

    if not request.data:
        return jsonify(RES_REQUIRE_BODY), 400

    return request_handlers.add_item(request.json)


@app.route('/shopping_list/<int:shopping_list_id>', methods=['PUT'])
def update_shopping_list(shopping_list_id):
    """Update shopping list. User can change the title or store name of the shopping list.

    Method: PUT
    Request header:
        required: Content-Type = application/json, Accept = application/json
    Request body: Request body should contain item 'name', for example:
        {
            "store_name": "FPT Software"
            , "title": "Fish"
        }
    Responses:
      500: If any exception occurs and failed to update shopping list.
      400: If bad request is sent.
      200: Update shopping list successfully.

    @:param shopping_list_id: ID of shopping list needed to be updated.
    @:return API response
    """
    if not request.is_json:
        return jsonify(RES_NOT_ACCEPTABLE), 400

    if not request.data:
        return jsonify(RES_REQUIRE_BODY), 400

    return request_handlers.update_shopping_list(shopping_list_id, request.json)


@app.route('/shopping_list/<int:shopping_list_id>', methods=['DELETE'])
def delete_shopping_list(shopping_list_id):
    """Delete shopping list. User can delete shopping list by ID.

    Method: DELETE
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to delete shopping list.
      400: If bad request is sent.
      200: Delete shopping list successfully.

    @:param shopping_list_id: ID of shopping list needed to be deleted.
    @:return API response
    """
    return request_handlers.delete_shopping_list(shopping_list_id)


@app.route('/item_shopping_list', methods=['POST'])
def add_item_to_shopping_list():
    """API to add items to shopping list DB.

    Method: POST
    Parameters: n/a
    Request header:
        required: Content-Type = application/json, Accept = application/json
    Request body: Request body should contain item 'shopping_list_id' and 'item_ids', for example:
        {
            "shopping_list_id": 2
            , "item_ids": [1,1,1,3,5,6,6,6]
        }
    Responses:
      500: If any exception occurs and failed to add item to shopping list.
      400: If bad request is sent.
      200: Add item to shopping list successfully.

    @:return Updated shopping list as JSON.
    """
    if not request.is_json:
        return jsonify(RES_NOT_ACCEPTABLE), 400

    if not request.data:
        return jsonify(RES_REQUIRE_BODY), 400

    return request_handlers.add_item_to_shopping_list(request.json)


@app.route('/all_shopping_lists', methods=['GET'])
def get_all_shopping_lists():
    """Get all shopping lists from DB.

    Method: GET
    Parameters: n/a
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to get all shopping lists.
      200: Get all shopping lists successfully.

    Example of returned result:
    [
        {
            "created_date": "Wed, 05 Sep 2018 16:25:23 GMT",
            "id": 2,
            "store_name": "FPT Education",
            "title": "Rice"
        },
        {
            "created_date": "Thu, 06 Sep 2018 01:23:53 GMT",
            "id": 3,
            "store_name": "FPT Software",
            "title": "Fish"
        }
    ]

    @:return All shopping lists as JSON.
    """
    return request_handlers.get_all_shopping_lists()


@app.route('/shopping_list/<title>', methods=['GET'])
def get_shopping_list_by_title(title):
    """Get all shopping lists from DB by title.

    Method: GET
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to get shopping lists by title.
      200: Get shopping lists successfully.

    Example of returned result:
    [
        {
            "created_date": "Wed, 05 Sep 2018 16:25:23 GMT",
            "id": 2,
            "store_name": "FPT Education",
            "title": "Rice"
        },
        {
            "created_date": "Thu, 06 Sep 2018 01:23:53 GMT",
            "id": 3,
            "store_name": "FPT Software",
            "title": "Fish"
        }
    ]

    @:param title: Title of shopping list.
    @:return All matched shopping lists as JSON.
    """
    return request_handlers.get_shopping_list_by_title(title)


@app.route('/shopping_list_by_title_keyword/<keyword>', methods=['GET'])
def get_shopping_list_by_keyword(keyword):
    """Get all shopping lists from DB by keyword.

    Example: Search for 'FPT' and get the list of all shopping lists
    with the word 'FPT' in the title such as 'FPT Software'.

    Method: GET
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to get shopping lists by keyword.
      200: Get shopping lists successfully.

    Example of returned result:
    [
        {
            "created_date": "Wed, 05 Sep 2018 16:25:23 GMT",
            "id": 2,
            "store_name": "FPT Education",
            "title": "Rice"
        },
        {
            "created_date": "Thu, 06 Sep 2018 01:23:53 GMT",
            "id": 3,
            "store_name": "FPT Software",
            "title": "Fish"
        }
    ]

    @:param title: Title to search for shopping lists.
    @:return All matched shopping lists as JSON.
    """
    return request_handlers.get_shopping_list_by_keyword(keyword)


@app.route('/shopping_list_by_item_id/<int:item_id>', methods=['GET'])
def get_shopping_list_by_item_id(item_id):
    """Get shopping lists from DB by item_id.

    Method: GET
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to get shopping lists by item_id.
      200: Get shopping lists successfully.

    Example of returned result:
    [
        {
            "created_date": "Wed, 05 Sep 2018 16:25:23 GMT",
            "id": 2,
            "store_name": "FPT Education",
            "title": "Rice"
        },
        {
            "created_date": "Thu, 06 Sep 2018 01:23:53 GMT",
            "id": 3,
            "store_name": "FPT Software",
            "title": "Fish"
        }
    ]

    @:param item_id: item_id to search for shopping lists.
    @:return All matched shopping lists as JSON.
    """
    return request_handlers.get_shopping_list_by_item_id(item_id)


@app.route('/shopping_list_by_item_name_keyword/<keyword>', methods=['GET'])
def get_shopping_list_by_item_name_keyword(keyword):
    """Get all shopping lists from DB by keyword of item name.

    Example: Search for “tomatoes” and get the list of all shopping lists with the word “tomatoes” in the item names.

    Method: GET
    Request header: n/a
    Request body: n/a
    Responses:
      500: If any exception occurs and failed to get shopping lists by keyword of item name.
      200: Get shopping lists successfully.

    Example of returned result:
    [
        {
            "created_date": "Wed, 05 Sep 2018 16:25:23 GMT",
            "id": 2,
            "store_name": "FPT Education",
            "title": "Rice"
        },
        {
            "created_date": "Thu, 06 Sep 2018 01:23:53 GMT",
            "id": 3,
            "store_name": "FPT Software",
            "title": "Fish"
        }
    ]

    @:param keyword: Keyword to search for shopping lists.
    @:return All matched shopping lists as JSON.
    """
    return request_handlers.get_shopping_list_by_item_name_keyword(keyword)
