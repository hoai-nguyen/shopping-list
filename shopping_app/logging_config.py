LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'custom': {
            'format': 'COS %(asctime)s %(levelname)s %(name)s (%(lineno)d) %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s|%(asctime)s|%(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S',
        },
    }
    , 'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'custom',
        }
    }
    , 'loggers': {
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'libs': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
    , "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}
