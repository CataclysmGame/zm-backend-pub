from typing import Optional

from sqlmodel import SQLModel, Field

from app.util import get_timestamp


class ScoreRecord(SQLModel, table=True):
    """
    Represents a score record inside the persistent database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(..., index=True, description='The user who submitted the score')
    score: int = Field(..., description='The score of the user')
    character: int = Field(..., description='The character chosen by the user')
    character_skin: Optional[str] = Field(default=None, description='The skin used by the user')
    timestamp: int = Field(default_factory=lambda: get_timestamp(),
                           description='The timestamp of the score submission')
    game_duration: int = Field(..., description='The duration of the game in seconds')
    game_version: str = Field(default='1.0.0', description='The version of the game')
