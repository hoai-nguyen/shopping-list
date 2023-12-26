import unittest

from apps.models import *
from apps.utils import *


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_json_to_object(self):
        passed_object = Item()
        payload = '{"name": "test_name"}'

        expected = Item()
        expected.name = "test_name"

        actual = convert_json_to_object(passed_object, payload)
        self.assertEqual(expected.name, actual.name)

    def test_convert_json_to_object_none(self):
        passed_object = Item()
        payload = None

        actual = convert_json_to_object(passed_object, payload)
        self.assertEqual(actual, None)

    def test_group_by_a_list(self):
        item_ids = [1, 3, 2, 3, 3]
        expected = {1: 1, 2: 1, 3: 3}

        actual = group_by_a_list(item_ids)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
