# -*- coding: utf-8 -*-

import json
import logging
from itertools import groupby

logger = logging.getLogger("utils")


def convert_json_to_object(passed_object, payload_data):
    """Convert JSON string of object to object


    @:param passed_object: Destination object.
    @:param payload_data: Input JSON string.
    @:return passed_object: The updated object.
    """
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
    """Group a list and output a dict(key, count).

    'key' set of the output dict will be the set of unique value in the input list.
    'count' of each 'key' will be the number of time the 'key' appears in the input list.

    @:param objects: List of items.
    @:return dict_key_2_count: A dict mapping from 'key' to 'count'
    """
    dict_key_2_count = {}
    for key, group in groupby(objects):
        if key not in dict_key_2_count:
            dict_key_2_count[key] = len(list(group))
        else:
            dict_key_2_count[key] = dict_key_2_count[key] + len(list(group))
    return dict_key_2_count
