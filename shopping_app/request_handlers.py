from flask import jsonify

from shopping_app import app, Session
from shopping_app.models import *
from shopping_app.utils import *


# TODO add logger


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


def add_shopping_list(payload):
    try:
        new_user = convert_json_to_object(ShoppingList(), json.dumps(payload))
        db_session = Session()
        db_session.add(new_user)
        db_session.commit()
    except Exception as ex:
        return jsonify({"message": "FAILED"}), 500

    return jsonify({"message": "SUCCESS"}), 200


def add_item(payload):
    try:
        new_item = convert_json_to_object(Item(), json.dumps(payload))
        db_session = Session()
        db_session.add(new_item)
        db_session.commit()
    except Exception as ex:
        return jsonify({"message": "FAILED"}), 500

    return jsonify({"message": "SUCCESS"}), 200


def update_shopping_list(shopping_list_id, payload):
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).all()

        for el in shopping_lists:
            el = edit_object_based_on_json(el, json.dumps(payload), ['id'])  # TODO remove util function

        db_session.commit()
    except:
        return jsonify({"message": "FAILED"}), 500

    return jsonify({"message": "SUCCESS"}), 200


def delete_shopping_list(shopping_list_id):
    try:
        db_session = Session()

        shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).all()
        for el in shopping_lists:
            db_session.delete(el)

        db_session.commit()
    except:
        return jsonify({"message": "FAILED"}), 500

    return jsonify({"message": "SUCCESS"}), 200


def add_item_to_shopping_list(payload):
    try:
        shopping_list_id = payload.get('shopping_list_id')  # TODO config
        item_ids = payload.get('item_ids')

        if not shopping_list_id or not item_ids:
            return jsonify({"message": "Shopping List ID and Item ID are required."}), 400

        db_session = Session()
        shopping_list = db_session.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).first()
        if not shopping_list:
            return jsonify({"message": "Invalid Shopping List ID."}), 400

        dict_id_2_count = group_by_a_list(item_ids)
        new_items = db_session.query(Item).filter(Item.id.in_(item_ids)).all()
        if not new_items or len(dict_id_2_count) > len(new_items):
            return jsonify({"message": "Invalid Item IDs."}), 400

        dict_id_2_new_item = dict([(x.id, x) for x in new_items])

        current_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.shopping_list_id == shopping_list.id
        ).all()

        for current_item in current_items:
            item_id = current_item.item_id
            if item_id and item_id in dict_id_2_new_item:
                current_item.quantity += dict_id_2_count[item_id]
                del dict_id_2_new_item[item_id]

        if len(dict_id_2_new_item) > 0:
            for item_id, item in dict_id_2_new_item.items():
                ShoppingListItem(shopping_list=shopping_list, item=item, quantity=dict_id_2_count[item_id])

        db_session.commit()

        # get updated Shopping List object as JSON string
        updated_shopping_list = shopping_list.as_dict()
        shopping_list_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.shopping_list_id == shopping_list.id
        ).all()
        updated_items = []
        for updated_item in shopping_list_items:
            updated_items.append(updated_item.as_dict())

        updated_shopping_list["items"] = updated_items

        return jsonify({"message": "SUCCESS", "updated_shopping_list": updated_shopping_list}), 200
    except:
        return jsonify({"message": "FAILED"}), 500


def get_all_shopping_lists():
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())
        return jsonify(dict_shopping_lists)
    except:
        return jsonify({"message": "FAILED"}), 500


def get_shopping_list_by_title(title):
        try:
            db_session = Session()
            shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.title == title).all()

            dict_shopping_lists = []
            for shopping_list in shopping_lists:
                dict_shopping_lists.append(shopping_list.as_dict())
            return jsonify(dict_shopping_lists)
        except:
            return jsonify({"message": "FAILED"}), 500


def get_shopping_list_by_keyword(keyword):
    try:
        db_session = Session()
        shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.title.contains(keyword)).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())
        return jsonify(dict_shopping_lists)
    except:
        return jsonify({"message": "FAILED"}), 500


def get_shopping_list_by_item_id(item_id):
    try:
        db_session = Session()
        shopping_list_items = db_session.query(ShoppingListItem).filter(
            ShoppingListItem.item_id == item_id
        ).all()
        shopping_list_ids = list(el.shopping_list_id for el in shopping_list_items)
        shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.id.in_(shopping_list_ids)).all()

        dict_shopping_lists = []
        for shopping_list in shopping_lists:
            dict_shopping_lists.append(shopping_list.as_dict())
        return jsonify(dict_shopping_lists)
    except:
        return jsonify({"message": "FAILED"}), 500


def get_shopping_list_by_item_name_keyword(keyword):
    try:
        db_session = Session()
        items = db_session.query(Item).filter(Item.name.contains(keyword)).all()
        if not items:
            return jsonify({}), 200

        item_ids = list(item.id for item in items)
        shopping_list_items = db_session.query(ShoppingListItem).filter(ShoppingListItem.item_id.in_(item_ids)).all()

        if shopping_list_items:
            shopping_list_ids = list(el.shopping_list_id for el in shopping_list_items)
            shopping_lists = db_session.query(ShoppingList).filter(ShoppingList.id.in_(shopping_list_ids)).all()

            if shopping_lists:
                dict_shopping_lists = []
                for shopping_list in shopping_lists:
                    dict_shopping_lists.append(shopping_list.as_dict())
                return jsonify(dict_shopping_lists), 200
    except:
        return jsonify({"message": "FAILED"}), 500

    return jsonify({}), 200
