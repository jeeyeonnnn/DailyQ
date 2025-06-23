from pydantic import BaseModel, json_schema

class SignUpRequest(BaseModel):
    user_id: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "jiyeon.park",
                "password": "1234"
            }
        }

class SignInRequest(BaseModel):
    user_id: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "jiyeon.park",
                "password": "1234"
            }
        }

class OnboardingRequest(BaseModel):
    nickname: str
    pet_type: int
    region_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "nickname": "무지개쿵야",
                "pet_type": 4,
                "region_id": 31
            }
        }

    
class GoogleSignInRequest(BaseModel):
    google_user_key: str

    class Config:
        json_schema_extra = {
            "example": {
                "google_user_key": "fjeiog35901wsd"
            }
        }