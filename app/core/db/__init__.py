from loguru import logger
from sqlalchemy_utils import database_exists, create_database
from sqlmodel import create_engine, SQLModel

from app.settings import settings

from app.core.db.models.score_record import ScoreRecord  # noqa
from app.core.db.models.banned_user import BannedUser  # noqa

connect_args = {}

if settings.DB_URL.startswith('sqlite'):
    connect_args['check_same_thread'] = False

engine = create_engine(
    settings.DB_URL,
    echo=settings.DB_ECHO,
    connect_args=connect_args,
)


def create_db_and_tables():
    if not database_exists(settings.DB_URL):
        if settings.CREATE_DB:
            create_database(settings.DB_URL)
        if settings.DEBUG:
            SQLModel.metadata.create_all(bind=engine)
            logger.info('Database tables created')
