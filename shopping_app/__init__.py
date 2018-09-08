# -*- coding: utf-8 -*-

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config, TestConfig
from shopping_app.database import *


def create_app(conf='any'):
    app = Flask(__name__)

    if conf == "TEST":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


from shopping_app import views, models
