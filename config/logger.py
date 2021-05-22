LOG_FILE = 'log.log'

LOGGER = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file",
        ],
    },
    "formatters": {
        "default": {
            "class": "logging.Formatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "filename": LOG_FILE,
            "mode": "a",
            "formatter": "json",
        },
    },
    "loggers": {
        "kafka": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}