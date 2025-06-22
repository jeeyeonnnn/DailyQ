from pydantic import BaseModel

class UserInfo(BaseModel):
    nickname: str
    level: int
    profile: str

class ChatDetail(BaseModel):
    content: str
    is_user_send: bool
    created_at: str