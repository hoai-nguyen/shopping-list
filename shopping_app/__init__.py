# -*- coding: utf-8 -*-

import logging.config

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Config
from shopping_app import logging_config

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
