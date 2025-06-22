from typing import List
from pydantic import BaseModel
from app.chat.dto.service import ChatDetail, UserInfo

class ChatRoomResponse(BaseModel):
    user_id: int
    nickname: str
    level: int
    profile: str
    last_message: str
    last_message_time: str
    unread_count: int

    class Config:
        json_schema_extra = {
            'example':   {
                "user_id": 10,
                "nickname": "나는멋쟁이",
                "level": 1,
                "profile": "ranking_1.png",
                "last_message": "이번주 정말 문제 멋있게 푸셨던군요? 정말 배우고 싶습니다. 멋져요 !! ???? ",
                "last_message_time": "27분 전",
                "unread_count": 0
            }
        }

class ChatDetailResponse(BaseModel):
    user_info: UserInfo
    chat_detail: List[ChatDetail]

    class Config:
        json_schema_extra = {
            'example': {
                "user_info": {
                    "nickname": "무지개쿵야",
                    "level": 1,
                    "profile": "chat_1.png"
                },
                "chat_detail": [
                    {
                    "content": "안녕하세요? 저는 무지개쿵야입니다! 새로 데일리큐에 오셨군요. 친하게 지내요 우리 ????",
                    "is_user_send": False,
                    "created_at": "PM 03:52"
                    },
                    {
                    "content": "이번주 정말 문제 멋있게 푸셨던군요? 정말 배우고 싶습니다. 멋져요 !! ???? ",
                    "is_user_send": False,
                    "created_at": "PM 03:57"
                    }
                ]
            }
        }