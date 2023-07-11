import sys

from loguru import logger

from app.settings import settings


def setup_logging():
    """
    Sets up the logging system.
    """
    logger.configure(handlers=[{
        'sink': sys.stderr if settings.LOG_TO_STDERR else sys.stdout,
        'serialize': settings.ENABLE_JSON_LOGGING,
        'level': settings.LOG_LEVEL.upper(),
    }])
