import json
from itertools import groupby


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


def group_by_a_list(objects):
    dict_key_2_count = {}
    for key, group in groupby(objects):
        if key not in dict_key_2_count:
            dict_key_2_count[key] = len(list(group))
        else:
            dict_key_2_count[key] = dict_key_2_count[key] + len(list(group))
    return dict_key_2_count