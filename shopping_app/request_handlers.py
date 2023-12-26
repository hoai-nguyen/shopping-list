# -*- coding: utf-8 -*-

from flask import jsonify
from sqlalchemy import func

from shopping_app import Session
from shopping_app.constants import *
from shopping_app.models import *
from shopping_app.utils import *

logger = logging.getLogger("handler")


def add_shopping_list(payload):
    """Service to add new shopping list to DB.

    Responses:
      500: If any exception occurs and failed to add shopping list to DB.
      400: If bad request is sent.
      200: Add shopping list to DB successfully.

    @:param payload: JSON information of new shopping list.
    @:return API response
    """
    try:
        new_shopping_list = \
            convert_json_to_object(ShoppingList(), json.dumps(payload))

        if not new_shopping_list or not new_shopping_list.title \
                or not new_shopping_list.store_name:
            return jsonify(RES_INVALID_BODY_SL), 400

        db_session = Session()
        if new_shopping_list.id:
            sl = db_session.query(ShoppingList) \
                .filter(ShoppingList.id == new_shopping_list.id).all()
            if len(sl) > 0:
                return jsonify(RES_DUPLICATED), 400

        db_session.add(new_shopping_list)
        db_session.commit()

    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500

    return jsonify(RES_SUCCESS), 200


def add_item(payload):
    """Service to add new item to DB.

    Responses:
      500: If any exception occurs and failed to add item to DB.
      400: If bad request is sent.
      200: Add item to DB successfully.

    @:param payload: JSON information of new item.
    @:return API response
    """
    try:
        new_item = convert_json_to_object(Item(), json.dumps(payload))

        if not new_item or not new_item.name:
            return jsonify(RES_INVALID_BODY_IT), 400

        db_session = Session()
        if new_item.id:
            sl = db_session.query(Item) \
                .filter(Item.id == new_item.id).all()
            if len(sl) > 0:
                return jsonify(RES_DUPLICATED), 400

        db_session.add(new_item)
        db_session.commit()

    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500

    return jsonify(RES_SUCCESS), 200


def update_shopping_list(shopping_list_id, payload):
    """Service to update shopping list.

    Responses:
      500: If any exception occurs and failed to update shopping list.
      400: If bad request is sent.
      200: Update shopping list successfully.

    @:param shopping_list_id: ID of shopping list needed to be updated.
    @:param payload: JSON information of 'store_name' and 'title' of shopping list.
    @:return API response
    """
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList) \
            .filter(ShoppingList.id == shopping_list_id) \
            .with_for_update(nowait=False).all()

        if not shopping_lists:
            return jsonify(RES_INVALID_SHOPPING_LIST_ID), 400

        new_title = payload.get(SL_TITLE)
        new_store_name = payload.get(SL_STORE_NAME)

        if not new_title and not new_store_name:
            return jsonify(RES_UPDATE_WITH_ALL_EMPTY_VALUES), 400

        for sl in shopping_lists:
            if new_title is not None:
                sl.title = new_title

            if new_store_name is not None:
                sl.store_name = new_store_name

        db_session.commit()
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500

    return jsonify(RES_SUCCESS), 200


def delete_shopping_list(shopping_list_id):
    """Service Delete shopping list.

    Responses:
      500: If any exception occurs and failed to delete shopping list.
      400: If bad request is sent.
      200: Delete shopping list successfully.

    @:param shopping_list_id: ID of shopping list needed to be deleted.
    @:return API response
    """
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList) \
            .filter(ShoppingList.id == shopping_list_id).all()

        if not shopping_lists:
            return jsonify(RES_INVALID_SHOPPING_LIST_ID), 400

        for el in shopping_lists:
            db_session.delete(el)

        db_session.commit()
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500

    return jsonify(RES_SUCCESS), 200


def add_item_to_shopping_list(payload):
    """Service to add items to shopping list.

    Responses:
      500: If any exception occurs and failed to add item to shopping list.
      400: If bad request is sent.
      200: Add item to shopping list successfully.

    @:param payload: JSON information of 'shopping_list_id' and 'item_ids'
    @:return Updated shopping list as JSON (if 200).
    """
    try:
        shopping_list_id = payload.get(REQ_SHOPPING_LIST_ID)
        item_ids = payload.get(REQ_ITEM_IDS)

        if not shopping_list_id or not item_ids:
            return jsonify(RES_REQUIRE_SHOPPING_LIST_ITEM_ID), 400

        db_session = Session()
        shopping_list = db_session.query(ShoppingList) \
            .filter(ShoppingList.id == shopping_list_id).first()

        if not shopping_list:
            return jsonify(RES_INVALID_SHOPPING_LIST_ID), 400

        dict_item_id_2_count = group_by_a_list(item_ids)
        new_items = db_session.query(Item).filter(Item.id.in_(item_ids)).all()

        if not new_items or len(dict_item_id_2_count) > len(new_items):
            return jsonify(RES_INVALID_ITEM_ID), 400

        dict_id_2_new_item = dict([(x.id, x) for x in new_items])

        current_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.shopping_list_id == shopping_list.id
        ).all()

        for current_item in current_items:
            item_id = current_item.item_id
            if item_id and item_id in dict_id_2_new_item:
                current_item.quantity += dict_item_id_2_count[item_id]
                del dict_id_2_new_item[item_id]

        # these items have never been added to the shopping list
        if len(dict_id_2_new_item) > 0:
            for item_id, item in dict_id_2_new_item.items():
                ShoppingListItem(shopping_list=shopping_list
                                 , item=item
                                 , quantity=dict_item_id_2_count[item_id])

        db_session.commit()

        # get updated Shopping List object as JSON string
        updated_shopping_list = shopping_list.as_dict()
        shopping_list_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.shopping_list_id == shopping_list.id
        ).all()

        updated_items = []
        for updated_item in shopping_list_items:
            updated_items.append(updated_item.as_dict())
        updated_shopping_list[SL_ITEMS] = updated_items

        return jsonify(updated_shopping_list), 200
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_all_shopping_lists():
    """Service to get all shopping lists from DB.

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
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())

        return jsonify(dict_shopping_lists)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_logs():
    try:
        db_session = Session()
        result = db_session.execute("SELECT * FROM user_logs")
        logs = [dict(row) for row in result]
        print(logs)
        # dict_shopping_lists = []
        # for log in logs:
        #     dict_shopping_lists.append(log)

        return jsonify(logs)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_shopping_list_by_title(title):
    """Service to get all shopping lists from DB by title.

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
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList) \
            .filter(func.lower(ShoppingList.title) == title.lower()).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())

        return jsonify(dict_shopping_lists)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_shopping_list_by_keyword(keyword):
    """Service to get all shopping lists from DB by keyword.

    Example: Search for 'FPT' and get the list of all shopping lists
    with the word 'FPT' in the title such as 'FPT Software'.

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
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList) \
            .filter(ShoppingList.title.contains(keyword)).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())

        return jsonify(dict_shopping_lists)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_shopping_list_by_item_id(item_id):
    """Service to get shopping lists from DB by item_id.

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
    try:
        db_session = Session()
        shopping_list_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.item_id == item_id
        ).all()
        shopping_list_ids \
            = list(el.shopping_list_id for el in shopping_list_items)
        shopping_lists = db_session.query(ShoppingList) \
            .filter(ShoppingList.id.in_(shopping_list_ids)).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())

        return jsonify(dict_shopping_lists)
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500


def get_shopping_list_by_item_name_keyword(keyword):
    """Get all shopping lists from DB by keyword of item name.

    Example: Search for “tomatoes” and get the list of all shopping lists with the word “tomatoes” in the item names.

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
    try:
        db_session = Session()
        items = db_session.query(Item) \
            .filter(Item.name.contains(keyword)).all()
        if not items:
            return jsonify({}), 200

        item_ids = list(item.id for item in items)
        shopping_list_items = db_session.query(ShoppingListItem) \
            .filter(ShoppingListItem.item_id.in_(item_ids)).all()

        if shopping_list_items:
            shopping_list_ids = \
                list(el.shopping_list_id for el in shopping_list_items)
            shopping_lists = db_session.query(ShoppingList) \
                .filter(ShoppingList.id.in_(shopping_list_ids)).all()

            if shopping_lists:
                dict_shopping_lists = []
                for shopping_list in shopping_lists:
                    dict_shopping_lists.append(shopping_list.as_dict())
                return jsonify(dict_shopping_lists), 200
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return jsonify(RES_FAILED), 500

    return jsonify({}), 200
