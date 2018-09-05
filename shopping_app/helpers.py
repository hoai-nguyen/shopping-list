import json
from flask import jsonify
from shopping_app import Session
from shopping_app.models import *


def add_shopping_list(payload):
    try:
        new_user = convert_json_to_object(ShoppingList(), json.dumps(payload))
        db_session = Session()
        db_session.add(new_user)
        db_session.commit()
    except Exception as ex:
        return jsonify({"message": "FAILED"}), 400

    return jsonify({"message": "SUCCESS"}), 200


def add_item(payload):
    try:
        new_item = convert_json_to_object(Item(), json.dumps(payload))
        db_session = Session()
        db_session.add(new_item)
        db_session.commit()
    except Exception as ex:
        return jsonify({"message": "FAILED"}), 400

    return jsonify({"message": "SUCCESS"}), 200


def convert_json_to_object(passed_object, payload_data):
    try:
        payload = json.loads(payload_data)
        for key, value in payload.items():
            if hasattr(passed_object, key):
                setattr(passed_object, key, value)
        return passed_object
    except:
        return None