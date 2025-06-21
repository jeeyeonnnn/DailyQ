from pydantic import BaseModel

class DailyQuizRequest(BaseModel):
    question_id: int
    choose: int

    class Config:
        json_schema_extra = {
            "example": {
                "question_id": 119,
                "choose": 3
            }
        }