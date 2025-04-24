import logging
from logging.config import dictConfig


LOG_FORMAT = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"

LOG_DEFAULT_HANDLERS = ["console"]

LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix) %(message)s",
            "use_colors": True,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - "
            "'%(request_line)s' %(status_code)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": LOG_DEFAULT_HANDLERS, "level": "INFO"},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
    "root": {"level": "INFO", "formatter": "verbose", "handlers": LOG_DEFAULT_HANDLERS},
}


# dictConfig(LOGGING)
logging.basicConfig(
    level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщения
    handlers=[
        logging.StreamHandler(),  # Вывод в консоль
        logging.FileHandler("app.log")  # Вывод в файл
    ]
)
logger = logging.getLogger(__name__)
