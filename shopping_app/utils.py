import logging

import json
from itertools import groupby

logger = logging.getLogger("utils")


def convert_json_to_object(passed_object, payload_data):
    try:
        payload = json.loads(payload_data)
        for key, value in payload.items():
            if hasattr(passed_object, key):
                setattr(passed_object, key, value)
        return passed_object
    except Exception as ex:
        logger.error(ex, exc_info=True)
        return None


def group_by_a_list(objects):
    dict_key_2_count = {}
    for key, group in groupby(objects):
        if key not in dict_key_2_count:
            dict_key_2_count[key] = len(list(group))
        else:
            dict_key_2_count[key] = dict_key_2_count[key] + len(list(group))
    return dict_key_2_count
