from typing import Optional

from pydantic.fields import Field

from .base_model import BaseModel


class ScoreSubmission(BaseModel):
    """
    Represents the submission of a highscore.
    """
    ticket: str = Field(..., description='The ticket of the game')
    user: str = Field(..., description='The user who submitted the score')
    score: int = Field(..., description='The score of the user')
    character_id: int = Field(..., description='The character chosen by the user')
    character_name: str = Field(..., description='Character name, included in the signature')
    character_skin: Optional[str] = Field(default=None, description='The skin used by the user')
    end_timestamp: int = Field(..., description='The timestamp of the end of the game')
    game_version: str = Field(default='1.0.0', description='The version of the game')
    signature: Optional[str] = Field(default=None, description='The game signature of the submission')
