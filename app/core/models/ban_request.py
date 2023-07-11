from typing import Optional

from pydantic import Field

from app.core.models.base_model import BaseModel


class BanRequest(BaseModel):
    """
    Represents a ban request performed by admins.
    """
    user: str = Field(..., description='The user to ban')
    reason: str = Field(..., description='The reason for the ban')
    duration: Optional[int] = Field(..., description='The duration of the ban in seconds')
    permanent: Optional[bool] = Field(..., description='Whether the ban is permanent')
    delete_scores: Optional[bool] = Field(..., description='Whether to delete the scores of the user')
