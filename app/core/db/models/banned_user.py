from typing import Optional

from sqlmodel import SQLModel, Field

from app.util import get_timestamp


class BannedUser(SQLModel, table=True):
    """
    Represents a banned user inside the persistent database.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user: str = Field(index=True, description='The user ID')
    reason: str = Field(..., description='The reason for the ban')
    timestamp: int = Field(default_factory=lambda: get_timestamp(), description='The timestamp of the ban')
    duration: int = Field(default=0, description='The duration of the ban in seconds')
