# Ref:
#  - https://stackoverflow.com/questions/7507825/where-is-a-complete-example-of-logging-config-dictconfig
#  - `arq.logs`

LOG_LEVEL = 'INFO'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s',
            'datefmt': '%Y-%M-%d %H:%M:%S'
        },
    },
    'handlers': {
        'default': {
            'level': LOG_LEVEL,
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'files/logs/arq.log',
            'mode': 'a',
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            # 'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'arq': {  # if __name__ == "__main__"
            'handlers': ['default'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}
