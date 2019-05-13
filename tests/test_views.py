from tests.base import *


class TestViews(BaseTestCase):

    def setUp(self):
        pass

    def test_api_return_200(self):
        with app.test_client() as c:
            rv = c.get('/my_api')
            print(rv)
            self.assertEqual("MESSAGE", rv.get_json())


if __name__ == '__main__':
    unittest.main()
