import os
import logging
import logging.config
import zipfile
from analysis_interface.settings import *
from logging.handlers import TimedRotatingFileHandler

# ----------------------------------------------------------------------
def setup_logging_from_dict(config, default_level=logging.INFO):
    if config:
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

# to rename old file
def namer(name):
    return os.path.join(LOG_DIR, os.path.basename(name)) + ".zip" 

# to compress old file
def rotator(source, dest):
    zf = zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED)
    zf.write(os.path.join(LOG_DIR, os.path.basename(source))) 
    zf.close()
    os.remove(source)


def create_logger(logger_name="root"):
    # get logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(CUSTOM_LEVEL)

    # create a file handler
    os.makedirs(LOG_DIR, exist_ok=True)
    handler = TimedRotatingFileHandler(\
        filename=os.path.join(LOG_DIR, CUSTOM_FILENAME), \
        when=CUSTOM_WHEN, \
        interval=int(CUSTOM_INTERVAL), \
        backupCount=int(CUSTOM_BACKUPCOUNT))
    handler.setLevel(CUSTOM_LEVEL)

    # create a logging format
    formatter = logging.Formatter(CUSTOM_FORMAT)
    handler.setFormatter(formatter)
    handler.rotator = rotator
    handler.namer = namer

    # add the handlers to the logger
    logger.addHandler(handler)

    clientip="default client"
    agent="default browser"
    url="default path"
    extra_attributes={'clientip': clientip, 'agent': agent, 'url': url}
    logger = logging.LoggerAdapter(logger, extra_attributes)

    return logger

# wrapper to log API access at INFO level
def log_info(msg, request):
    try:
        logger = logging.getLogger("root")
       
        clientip = request.environ.get('HTTP_X_FORWARDED_FOR') \
            or request.environ['REMOTE_ADDR'] \
            or request.remote_addr
        agent = request.user_agent.platform + "/" + request.user_agent.browser
        url = request.method + " " + request.url
        extra_attributes={'clientip': clientip, 'agent': agent, 'url': url}
        
        logger.info(msg, extra=extra_attributes)

    except Exception as ex:
        logger.error(ex, exc_info=True)
    
setup_logging_from_dict(LOGGING)
logger = create_logger()

