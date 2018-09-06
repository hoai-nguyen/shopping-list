from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from shopping_app import db
from flask import Flask


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('config.TestConfig')

        with app.app_context():
            test_db = SQLAlchemy(app)
            engine = test_db.engine
            session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
            base = declarative_base()
            base.metadata.create_all(bind=engine)
            session().commit()

        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
