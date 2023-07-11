from pydantic import BaseModel


class Game(BaseModel):
    ticket: str
    score: int
    timestamp: str
