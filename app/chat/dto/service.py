from pydantic import BaseModel

class UserInfo(BaseModel):
    user_id: int
    nickname: str
    level: int
    profile: str

class ChatDetail(BaseModel):
    user_id: int
    content: str
    is_user_send: bool
    created_at: str