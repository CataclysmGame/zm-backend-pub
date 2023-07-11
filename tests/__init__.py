import pytest
from sqlmodel import SQLModel

from app.core.db import engine


@pytest.fixture()
def test_db():
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)
