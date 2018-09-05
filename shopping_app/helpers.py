import json
from flask import jsonify
from shopping_app import app, Session
from shopping_app.models import *

# TODO add logger


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


def convert_json_to_object(passed_object, payload_data):
    try:
        payload = json.loads(payload_data)
        for key, value in payload.items():
            if hasattr(passed_object, key):
                setattr(passed_object, key, value)
        return passed_object
    except:     # TODO specify class
        return None


def edit_object_based_on_json(passed_object, payload_data, skip_list):
    try:
        payload = json.loads(payload_data)
        for key, value in payload.items():
            if key not in skip_list and value is not None:
                if hasattr(passed_object, key):
                    setattr(passed_object, key, value)
        return passed_object
    except:
        return None


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
        if not payload:
            jsonify({"message": "Shopping List ID and Item ID are required."}), 400

        shopping_list_id = payload.get('shopping_list_id')  # TODO config
        item_ids = payload.get('item_ids')

        if not shopping_list_id or not item_ids:
            return jsonify({"message": "Shopping List ID and Item ID are required."}), 400  # TODO refactor responses

        db_session = Session()
        shopping_list = db_session.query(ShoppingList).filter(ShoppingList.id == shopping_list_id).first()
        new_items = db_session.query(Item).filter(Item.id.in_(item_ids)).all()

        current_items = shopping_list.items
        if not current_items:
            for new_item in new_items:
                ShoppingListItem(shopping_list=shopping_list, item=new_item, quantity=1)
        else:
            for new_item in new_items:
                found = False
                for current_item in current_items:
                    if new_item.__eq__(current_item):
                        found = True
                        shopping_list_item = db_session.query(ShoppingListItem).filter(
                            ShoppingListItem.item_id == current_item.id,
                            ShoppingListItem.shopping_list_id == shopping_list.id
                        ).first()
                        if shopping_list_item.quantity:
                            shopping_list_item.quantity += 1
                        break

                if not found:
                    ShoppingListItem(shopping_list=shopping_list, item=new_item, quantity=1)

        db_session.commit()

        return jsonify({"message": "SUCCESS"}), 200
    except:
        return jsonify({"message": "FAILED"}), 500
