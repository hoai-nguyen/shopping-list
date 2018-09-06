# -*- coding: utf-8 -*-

import logging.config
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config
from shopping_app import logging_config
from shopping_app.database import init_engine

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

engine = db.engine
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


if logging_config.LOGGING:
    logging.config.dictConfig(logging_config.LOGGING)
else:
    logging.basicConfig(level=logging.INFO)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


from shopping_app import views, models


def create_app(db_uri='any'):
    app = Flask(__name__)
    app.config.from_object('shopping_app.default_config')
    app.config.from_pyfile(os.path.join(app.instance_path, 'config.py'))

    print(app.config)

    if db_uri == 'Test':
        init_engine(app.config['TEST_DATABASE_URI'])
    else:
        init_engine(app.config['DATABASE_URI'])

    if logging_config.LOGGING:
        logging.config.dictConfig(logging_config.LOGGING)
    else:
        logging.basicConfig(level=logging.INFO)

    return app
