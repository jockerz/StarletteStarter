import logging

logger = logging.getLogger('uvicorn.error')


def get_logger() -> logging.Logger:
    return logger
