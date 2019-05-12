import unittest

from analysis_interface.models import *
from analysis_interface.utils import *


class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_convert_json_to_object(self):
        passed_object = KeyWord()
        payload = '{"name": "test_name"}'

        expected = KeyWord()
        expected.name = "test_name"

        actual = convert_json_to_object(passed_object, payload)
        self.assertEqual(expected.name, actual.name)

    def test_convert_json_to_object_none(self):
        passed_object = KeyWord()
        payload = None

        actual = convert_json_to_object(passed_object, payload)
        self.assertEqual(actual, None)

    def test_group_by_a_list(self):
        KeyWord_ids = [1, 3, 2, 3, 3]
        expected = {1: 1, 2: 1, 3: 3}

        actual = group_by_a_list(KeyWord_ids)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
