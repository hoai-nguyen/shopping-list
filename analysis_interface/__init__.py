# -*- coding: utf-8 -*

import os
import logging
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config, TestConfig
from analysis_interface.utils_logging import logger, log_info
from analysis_interface.database import init_engine

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


@app.before_request
def action_before_request():
    try:
        log_info("BEFORE REQUEST MESSAGE", request)
        logger.info("ANOTHER BEFORE REQUEST MESSAGE")
    except Exception as ex:
        logger.error(ex, exc_info=True)


@app.after_request
def action_after_request(response):
    try:
        log_info("AFTER REQUEST MESSAGE", request)
        logger.info("ANOTHER AFTER REQUEST MESSAGE")
    except Exception as ex:
        logger.error(ex, exc_info=True)

    return response


from analysis_interface import views
