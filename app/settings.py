import os
from typing import Optional, List

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    # General
    PROJECT_NAME: str = 'CataclysmZeroMissionGameServer'

    DEBUG: bool = False

    # Logging
    LOG_LEVEL: str = 'info'
    ENABLE_JSON_LOGGING: bool = False
    LOG_TO_STDERR: bool = True

    # Storage
    DB_URL: str = 'sqlite:///cataclysm-zm.db'
    DB_ECHO: bool = False

    CREATE_DB: bool = True

    CACHE_URL: str = 'memory://'

    # Sentry
    SENTRY_DSN: Optional[AnyHttpUrl] = None
    SENTRY_SAMPLE_RATE: float = 1.0
    SENTRY_MAX_BREADCRUMBS: int = 100

    # Prometheus
    PROMETHEUS_ENABLED: bool = False
    PROMETHEUS_METRICS_ENDPOINT: str = '/metrics'

    # API
    API_HOST: str = 'localhost'
    API_PORT: int = 7073
    API_RELOAD: bool = False

    API_V1_PREFIX: str = '/api/v1'

    ENVDUMP_ENABLED: bool = False

    MAX_LEADERBOARD_LEN: int = 100

    # Security
    CORS_ORIGINS: Optional[List[str]] = None
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ['*']
    CORS_ALLOW_HEADERS: List[str] = ['*']

    TICKETS_TTL: int = 60 * 60 * 3  # 3 hours

    # Domain
    GAME_TICKET_LEN: int = 20

    # Anti-cheat
    MAX_DURATION_DRIFT_SECONDS: int = 10
    MAX_SCORE_DELTA: int = 100

    GAME_ADDRESS: str = '0x92Bd0A7FD1D91c3Cfd5EcaA1399A0826B56e3d65'

    MAX_SCORES_PER_CHARACTER: int = 1

    class Config:
        case_sensitive = False
        env_file = os.getenv('DOT_ENV_FILE', '.env')
        env_file_encoding = os.getenv('DOT_ENV_FILE_ENCODING', 'utf-8')


settings = Settings()


def log_settings() -> None:
    from loguru import logger
    logger.debug('Settings: {}', settings)
