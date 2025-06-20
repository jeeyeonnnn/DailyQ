from pydantic import BaseModel

class SignInResponse(BaseModel):
    message: str
    access_token: str
    is_signup_done: bool

    class Config:
        json_schema_extra = {
            "example": {
                "message": "로그인이 완료되었습니다.",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE5NTc5MTMsImlhdCI6MTc1MDQyMTkxMywic3ViIjoxfQ.DpRhMsJ9TfZcMPFpeI8bQ15p4Me2OoVnDNyWfhKoE68",
                "is_signup_done": False
            }
        }