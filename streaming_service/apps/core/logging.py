import logging
from logging.config import dictConfig

LOG_FORMAT = "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Не отключать существующие логгеры
    "formatters": {
        "verbose": {"format": LOG_FORMAT},
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(message)s",
            "use_colors": True,  # Использовать цвета в консоли
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
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
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "apps.log",  # Файл для записи логов
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {  # Корневой логгер
            "handlers": ["console", "file"],  # Вывод в консоль и файл
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["access", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}



dictConfig(LOGGING)
# logging.basicConfig(
#     level=logging.INFO,  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Формат сообщения
#     handlers=[
#         logging.StreamHandler(),  # Вывод в консоль
#         logging.FileHandler("apps.log")  # Вывод в файл
#     ]
# )
logger = logging.getLogger(__name__)
