# -*- coding: utf-8 -*-

# response messages
RES_REQUIRE_BODY = {"message": "Require body."}
RES_NOT_ACCEPTABLE = {"message": "Support only content-type = application/json."}
RES_FAILED = {"message": "FAILED"}
RES_SUCCESS = {"message": "OK"}
RES_REQUIRE_SHOPPING_LIST_ITEM_ID = {"message": "Shopping List ID and Item ID are required."}
RES_INVALID_SHOPPING_LIST_ID = {"message": "Invalid Shopping List ID."}
RES_INVALID_ITEM_ID = {"message": "Invalid Item IDs."}
RES_FAILED_TO_ADD_SHOPPING_LIST= {"message": "Failed to add Shopping List."}
RES_UPDATE_WITH_ALL_EMPTY_VALUES= {"message": "Try to update with both empty title and store_name."}
RES_FAILED_TO_PARSE_JSON = {"message": "Failed to parse JSON to object."}
RES_DUPLICATED = {"message": "Duplicated ID."}
RES_INVALID_BODY_SL = {"message": "Shopping List title/store_name is missing or empty"}
RES_INVALID_BODY_IT = {"message": "Item name is missing or empty"}

# request body fields
REQ_SHOPPING_LIST_ID = "shopping_list_id"
REQ_ITEM_IDS = "item_ids"

# shopping list fields
SL_TITLE = "title"
SL_STORE_NAME = "store_name"
SL_ITEMS = "items"

# logging messages
MSG_FAILED_TO_ADD_SHOPPING_LIST = 'Failed to add shopping list: '
MSG_FAILED_TO_PARSE_JSON = "Failed to parse JSON to object."
