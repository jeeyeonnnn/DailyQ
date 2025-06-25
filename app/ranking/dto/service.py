from typing import Union
from pydantic import BaseModel

class Ranking(BaseModel):
    ranking: Union[int, str]
    nickname: str
    level: int
    profile: str
    question_count: int
    correct_rate: float