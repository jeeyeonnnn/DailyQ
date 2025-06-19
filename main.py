from fastapi import FastAPI
from app.region.endpoint import router as region_router

app = FastAPI(title="DailyQ API", version="1.0.0")

@app.get("/", tags=["☑️ Health Check"])
def read_root():
    return {"message": "Hello, DailyQ!"}

app.include_router(region_router)