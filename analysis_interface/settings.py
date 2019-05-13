import os
import logging

LOG_DIR="logs"

# TimedRotatingFileHandler parameters
CUSTOM_FORMAT='%(asctime)s - %(levelname)s - %(clientip)s - %(message)s - %(agent)s - %(url)s'
CUSTOM_LEVEL=logging.INFO
CUSTOM_FILENAME='access.log'
CUSTOM_WHEN='s'
CUSTOM_INTERVAL='2'
CUSTOM_BACKUPCOUNT=24
CUSTOM_ENCODING=None
CUSTOM_DELAY=False
CUSTOM_UTC=False
CUSTOM_ATTIME=None


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple_format': {
            'format': '%(asctime)s %(levelname)s %(name)s (%(lineno)d) %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple_format',
        },
        'to_compressed_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join('logs', 'access.log'),
            "when": "s",
            "interval": 2,
            "backupCount": 20
        }
    },
    'loggers': {
        'sample_logger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ['console']
    }
}
