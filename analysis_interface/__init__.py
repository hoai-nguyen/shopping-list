# -*- coding: utf-8 -*-

import os
import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
from flask import Flask, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import zipfile
from config import Config, TestConfig
from analysis_interface.database import *
from analysis_interface.settings_logging import *


def namer(name):
    return os.path.join(LOG_DIR, os.path.basename(name)) + ".zip" # output

def rotator(source, dest):
    zf = zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED)
    zf.write(os.path.join(LOG_DIR, os.path.basename(source))) # input file
    zf.close()
    os.remove(source)


# create logger
logger = logging.getLogger("root")
logger.setLevel(CUSTOM_LEVEL)

# # create a file handler
os.makedirs(LOG_DIR, exist_ok=True)
handler = TimedRotatingFileHandler(\
    filename=os.path.join(LOG_DIR, CUSTOM_FILENAME), \
    when=CUSTOM_WHEN, \
    interval=int(CUSTOM_INTERVAL), \
    backupCount=int(CUSTOM_BACKUPCOUNT))
handler.setLevel(CUSTOM_LEVEL)

# # create a logging format
# formatter = logging.Formatter(CUSTOM_FORMAT)
formatter = logging.Formatter('CUSTOM: %(asctime)s %(levelname)s %(name)s (%(lineno)d) %(message)s')
handler.setFormatter(formatter)
handler.rotator = rotator
handler.namer = namer

# # add the handlers to the logger
logger.addHandler(handler)
clientip="localhost"
agent="n/a"
url="/api"
test_att=""
extra_attributes={'test_att': test_att, 'clientip': clientip, 'agent': agent, 'url': url}
logger = logging.LoggerAdapter(logger, extra_attributes)

# ----------------------------------------------------------------------
def setup_logging_from_dict(config, default_level=logging.INFO):
    if config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

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
setup_logging_from_dict(LOGGING)


@app.before_request
def action_before_request():
    try:
        logger = logging.getLogger("root")
        os.makedirs('logs', exist_ok=True)
        
        clientip = request.environ['REMOTE_ADDR']
        agent = request.user_agent.platform + "/" + request.user_agent.browser
        url = request.method + " " + request.url
        extra_attributes={'test_att': 123, 'clientip': clientip, 'agent': agent, 'url': url}

        # logger = logging.LoggerAdapter(logger, extra_attributes)
        logger.info("BEFORE REQUEST MESSAGE", extra=extra_attributes)
        # logger.info("ANOTHER BEFORE REQUEST MESSAGE")
        # app.logger.info("MESSAGE APP")
        # log_info("BEFORE REQUEST MESSAGE")
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            print(request.environ['REMOTE_ADDR'])
        else:
            print(request.environ['HTTP_X_FORWARDED_FOR'])
        # print(1/0)
        
    except Exception as ex:
        logger.error(ex)
        # app.logger.info(ex)


def log_info(msg):
    try:
        logger = logging.getLogger("root")
        os.makedirs('logs', exist_ok=True)
        
        clientip = request.remote_addr
        agent = request.user_agent.platform + "/" + request.user_agent.browser
        url = request.method + " " + request.url
        extra_attributes={'clientip': clientip, 'agent': agent, 'url': url}
        
        logger.info(msg, extra=extra_attributes)

    except Exception as ex:
        logger.error(ex)
    

@app.after_request
def action_after_request(response):
    try:
        os.makedirs('logs', exist_ok=True)
        extra_attributes={'clientip': request.remote_addr, \
            'agent': request.user_agent.platform + "/" + request.user_agent.browser, \
            'url': request.method + " " + request.url + " " + response.status}
        logger.info("AFTER REQUEST MESSAGE", extra=extra_attributes)
        # print(1/0)
        # logger.info("ANOTHER AFTER REQUEST MESSAGE")
    except Exception as ex:
        logger.error(ex)

    return response


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


from analysis_interface import views, models
