from pydantic import BaseModel

class MainRegion(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "서울특별시"
            }
        }

class SubRegion(BaseModel):
    id: int
    name: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "강남구"
            }
        }