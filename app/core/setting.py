import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv("./app/core/.env")


class Setting:
    DB_USER = os.environ.get("DB_USER")
    DB_PW = os.environ.get("DB_PW")
    DB_PORT = os.environ.get("DB_PORT")
    DB_HOST = os.environ.get("DB_HOST")

    JWT_SECRET = os.environ.get("JWT_SECRET")
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
    
    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
    S3_REGION = os.environ.get("S3_REGION")

    @property
    def get_db_url(self):
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PW}@{self.DB_HOST}:{self.DB_PORT}/dailyq' \
               f'?charset=utf8'

    def get_exam_image_url(self, count: Optional[int] = None):
        if count is None:
            return f'https://{self.S3_BUCKET_NAME}.s3.{self.S3_REGION}.amazonaws.com/no_exam.png'
        else:
            return f'https://{self.S3_BUCKET_NAME}.s3.{self.S3_REGION}.amazonaws.com/exam/exam_result_{count}.png'

setting = Setting()