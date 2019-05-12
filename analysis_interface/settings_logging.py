import os
import logging

LOG_DIR="logs"

CUSTOM_FORMAT='%(test_att)s - %(asctime)s - %(levelname)s - %(clientip)s - %(message)s - %(agent)s - %(url)s'
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
        'custom': {
            'format': 'CUSTOM: %(asctime)s %(levelname)s %(name)s (%(lineno)d) %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s|%(asctime)s|%(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
        },
        'to_file': {
            'formatter': 'custom',
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join('logs', 'history.log'),
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
        },
        'django': {
            'handlers': ['console', 'to_file'],
            'level': 'ERROR',
        }
    },
    "root": {
        "level": "INFO",
        "handlers": []
    }
}
