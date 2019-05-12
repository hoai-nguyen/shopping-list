from analysis_interface.request_handlers import *
from tests.base import *


class TestRequestHandlers(BaseTestCase):

    def setUp(self):
        db_session = Session()
        sl_1 = db_session.query(ShoppingList).filter(ShoppingList.id == -1).all()
        sl_2 = db_session.query(ShoppingList).filter(ShoppingList.id == -2).all()
        sl_4 = db_session.query(ShoppingList).filter(ShoppingList.id == -4).first()
        it_1 = db_session.query(KeyWord).filter(KeyWord.id == -1).all()
        it_2 = db_session.query(KeyWord).filter(KeyWord.id == -2).all()
        it_sl_22 = db_session.query(ShoppingListKeyWord).filter(
            ShoppingListKeyWord.shopping_list_id == -2
            , ShoppingListKeyWord.KeyWord_id == -2
        ).all()
        it_sl_41 = db_session.query(ShoppingListKeyWord).filter(
            ShoppingListKeyWord.shopping_list_id == -4
            , ShoppingListKeyWord.KeyWord_id == -1
        ).first()

        payload_sl_1 = {"id": -1, "title": "test_title", "store_name": "test_store"}
        payload_sl_2 = {"id": -2, "title": "test_title_2", "store_name": "test_store"}
        payload_sl_4 = {"id": -4, "title": "test_title_4", "store_name": "test_store"}
        payload_it_1 = {"id": -1, "name": "test_name_1"}
        payload_it_2 = {"id": -2, "name": "test_name"}

        if not sl_1:
            add_shopping_list(payload_sl_1)
        if not sl_2:
            add_shopping_list(payload_sl_2)
        if not sl_4:
            add_shopping_list(payload_sl_4)
        if not it_1:
            add_KeyWord(payload_it_1)
        if not it_2:
            add_KeyWord(payload_it_2)
        if it_sl_22:
            for el in it_sl_22:
                db_session.delete(el)
            db_session.commit()
        if not it_sl_41:
            KeyWord = db_session.query(KeyWord).filter(KeyWord.id == -1).first()
            s4 = db_session.query(ShoppingList).filter(ShoppingList.id == -4).first()
            ShoppingListKeyWord(shopping_list=s4
                             , KeyWord=KeyWord
                             , quantity=1)
            db_session.commit()

    def tearDown(self):
        pass

    def test_add_shopping_list_200(self):
        payload = {"title": "test_title", "store_name": "test_store_name"}
        expected = {'message': 'OK', 'status': 200}

        res = add_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_shopping_list_400_missing(self):
        payload = {"id": -1, "title": "", "store_name": "test_store_name"}

        expected = RES_INVALID_BODY_SL
        expected['status'] = 400

        res = add_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_shopping_list_400_dup(self):
        payload = {"id": -1, "title": "test_title", "store_name": "test_store_name"}

        expected = RES_DUPLICATED
        expected['status'] = 400

        res = add_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_KeyWord_200(self):
        payload = {"name": "name"}

        expected = {'message': 'OK', 'status': 200}
        res = add_KeyWord(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_KeyWord_400_invalid_body(self):
        payload = None

        expected = RES_INVALID_BODY_IT
        expected['status'] = 400

        res = add_KeyWord(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_KeyWord_400_dup(self):
        payload = {"id": -1, "name": "test_name"}

        expected = RES_DUPLICATED
        expected['status'] = 400

        res = add_KeyWord(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_update_shopping_list_200(self):
        shopping_list_id = -2
        payload = {"title": "new_title", "store_name": "new_store_name"}

        expected = {'message': 'OK', 'status': 200}
        res = update_shopping_list(shopping_list_id, payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_update_shopping_list_400(self):
        shopping_list_id = -10
        payload = None

        expected = RES_INVALID_SHOPPING_LIST_ID
        expected['status'] = 400

        res = update_shopping_list(shopping_list_id, payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_update_shopping_list_400_empty(self):
        shopping_list_id = -2
        payload = {"title": "", "store_name": ""}

        expected = RES_UPDATE_WITH_ALL_EMPTY_VALUES
        expected['status'] = 400

        res = update_shopping_list(shopping_list_id, payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_update_shopping_list_500(self):
        shopping_list_id = -2
        payload = None

        expected = RES_FAILED
        expected['status'] = 500

        res = update_shopping_list(shopping_list_id, payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_delete_shopping_list_200(self):
        shopping_list_id = -1
        payload = {"title": "test_title", "store_name": "test_store_name"}
        add_shopping_list(payload)

        expected = RES_SUCCESS
        expected['status'] = 200
        res = delete_shopping_list(shopping_list_id)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_delete_shopping_list_400(self):
        shopping_list_id = -3

        expected = RES_INVALID_SHOPPING_LIST_ID
        expected['status'] = 400

        res = delete_shopping_list(shopping_list_id)

        actual = json.loads(res[0].get_data(as_text=True))
        actual['status'] = res[1]

        self.assertEqual(expected, actual)

    def test_add_KeyWord_to_shopping_list_200(self):
        payload = {"shopping_list_id": -2, "KeyWord_ids": [-1, -1, -2]}
        expected = 200

        res = add_KeyWord_to_shopping_list(payload)

        actual = res[1]
        self.assertEqual(expected, actual)

    def test_add_KeyWord_to_shopping_list_400_missing_id(self):
        payload = {"shopping_list_id": -2, "KeyWord_ids": []}
        expected = RES_REQUIRE_SHOPPING_LIST_KeyWord_ID
        expected['status'] = 400

        res = add_KeyWord_to_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual["status"] = res[1]
        self.assertEqual(expected, actual)

    def test_add_KeyWord_to_shopping_list_400_invalid_sl(self):
        payload = {"shopping_list_id": -20, "KeyWord_ids": [-1]}
        expected = RES_INVALID_SHOPPING_LIST_ID
        expected['status'] = 400

        res = add_KeyWord_to_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual["status"] = res[1]
        self.assertEqual(expected, actual)

    def test_add_KeyWord_to_shopping_list_400_invalid_it(self):
        payload = {"shopping_list_id": -2, "KeyWord_ids": [-20]}
        expected = RES_INVALID_KeyWord_ID
        expected['status'] = 400

        res = add_KeyWord_to_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual["status"] = res[1]
        self.assertEqual(expected, actual)

    def test_add_KeyWord_to_shopping_list_500(self):
        payload = None
        expected = RES_FAILED
        expected['status'] = 500

        res = add_KeyWord_to_shopping_list(payload)

        actual = json.loads(res[0].get_data(as_text=True))
        actual["status"] = res[1]
        self.assertEqual(expected, actual)

    def test_get_all_shopping_lists_200(self):
        expected = 200
        res = get_all_shopping_lists()
        self.assertEqual(expected, res.status_code)

    def test_get_shopping_list_by_title_200(self):
        title = "test_title_4"
        expected = 200
        res = get_shopping_list_by_title(title)
        self.assertEqual(expected, res.status_code)

    def test_get_shopping_list_by_title_500(self):
        title = None
        expected = 500
        res = get_shopping_list_by_title(title)
        self.assertEqual(expected, res[1])

    def test_get_shopping_list_by_keyword_200(self):
        title = "title_4"
        expected = 200
        res = get_shopping_list_by_keyword(title)
        self.assertEqual(expected, res.status_code)

    def test_get_shopping_list_by_KeyWord_id_200(self):
        KeyWord_id = -1
        expected = 200
        res = get_shopping_list_by_KeyWord_id(KeyWord_id)
        self.assertEqual(expected, res.status_code)

    def test_get_shopping_list_by_KeyWord_name_keyword_200(self):
        keyword = "name_1"
        expected = 200
        res = get_shopping_list_by_KeyWord_name_keyword(keyword)
        self.assertEqual(expected, res[1])

    def test_get_shopping_list_by_KeyWord_name_keyword_500(self):
        keyword = None
        expected = 500
        res = get_shopping_list_by_KeyWord_name_keyword(keyword)
        self.assertEqual(expected, res[1])


if __name__ == '__main__':
    unittest.main()
