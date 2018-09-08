from shopping_app.constants import *
from tests.base import *


class TestViews(BaseTestCase):

    def setUp(self):
        pass

    def test_add_shopping_list_400_mime_type(self):
        with app.test_client() as c:
            rv = c.post('/shopping_list')
            self.assertEqual(RES_NOT_ACCEPTABLE, rv.get_json())

    def test_add_shopping_list_400_body(self):
        with app.test_client() as c:
            rv = c.post('/shopping_list', headers={'content-type': 'application/json'})
            self.assertEqual(RES_REQUIRE_BODY, rv.get_json())

    def test_add_shopping_list_400_missing_field(self):
        body = {'title': 'flask'}
        with app.test_client() as c:
            rv = c.post('/shopping_list', json=body)
            self.assertEqual(RES_INVALID_BODY_SL, rv.get_json())

    def test_add_add_item_400_mime_type(self):
        with app.test_client() as c:
            rv = c.post('/item')
            self.assertEqual(RES_NOT_ACCEPTABLE, rv.get_json())

    def test_add_add_item_400_body(self):
        with app.test_client() as c:
            rv = c.post('/item', headers={'content-type': 'application/json'})
            self.assertEqual(RES_REQUIRE_BODY, rv.get_json())

    def test_add_add_item_400_missing_field(self):
        body = {'named': 'flask'}
        with app.test_client() as c:
            rv = c.post('/item', json=body)
            self.assertEqual(RES_INVALID_BODY_IT, rv.get_json())

    def test_update_shopping_list_400_mime_type(self):
        with app.test_client() as c:
            rv = c.put('/shopping_list/1')
            self.assertEqual(RES_NOT_ACCEPTABLE, rv.get_json())

    def test_update_shopping_list_400_body(self):
        with app.test_client() as c:
            rv = c.put('/shopping_list/1', headers={'content-type': 'application/json'})
            self.assertEqual(RES_REQUIRE_BODY, rv.get_json())

    def test_update_shopping_list_400_missing_field(self):
        body = {'titfle': 'flask'}
        with app.test_client() as c:
            rv = c.put('/shopping_list/1', json=body)
            self.assertEqual(RES_UPDATE_WITH_ALL_EMPTY_VALUES, rv.get_json())

    def test_delete_shopping_list_400_invalid_id(self):
        with app.test_client() as c:
            c.delete('/shopping_list/1000')
            rv = c.delete('/shopping_list/1000')
            self.assertEqual(RES_INVALID_SHOPPING_LIST_ID, rv.get_json())

    def test_add_item_to_shopping_list_400_mime_type(self):
        with app.test_client() as c:
            rv = c.post('/item_shopping_list')
            self.assertEqual(RES_NOT_ACCEPTABLE, rv.get_json())

    def test_add_item_to_shopping_list_400_body(self):
        with app.test_client() as c:
            rv = c.post('/item_shopping_list', headers={'content-type': 'application/json'})
            self.assertEqual(RES_REQUIRE_BODY, rv.get_json())

    def test_add_item_to_shopping_list_400_missing_field(self):
        body = {'id': '1'}
        with app.test_client() as c:
            rv = c.post('/item_shopping_list', json=body)
            self.assertEqual(RES_REQUIRE_SHOPPING_LIST_ITEM_ID, rv.get_json())

    def test_get_all_shopping_lists(self):
        with app.test_client() as c:
            rv = c.post('/all_shopping_lists')
            self.assertNotEquals(RES_FAILED, rv.get_json())

    def test_get_shopping_list_by_title(self):
        with app.test_client() as c:
            rv = c.post('/all_shopping_lists/title')
            self.assertNotEquals(RES_FAILED, rv.get_json())

    def test_get_shopping_list_by_item_id(self):
        with app.test_client() as c:
            rv = c.get('/shopping_list_by_item_id/1')
            self.assertNotEquals(RES_FAILED, rv.get_json())

    def test_get_shopping_list_by_item_name_keyword(self):
        with app.test_client() as c:
            rv = c.get('/shopping_list_by_item_name_keyword/1')
            self.assertNotEquals(RES_FAILED, rv.get_json())


if __name__ == '__main__':
    unittest.main()
