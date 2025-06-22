from pydantic import BaseModel

class ChatSendRequest(BaseModel):
    user_id: int
    content: str

    class Config:
        json_schema_extra = {
            'example': {
                "user_id": 10,
                "content": "안녕하세요? 저는 무지개쿵야입니다! 새로 데일리큐에 오셨군요. 친하게 지내요 우리 !",
            }
        }