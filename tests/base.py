import unittest

from flask_testing import TestCase

from shopping_app import app, db, create_app


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        self.app = create_app("TEST")
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    unittest.main()