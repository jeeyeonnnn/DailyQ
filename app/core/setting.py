import os
from typing import Optional
from dotenv import load_dotenv
import boto3

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
    S3_ACCESS_KEY = os.environ.get("S3_ACCESS_KEY")
    S3_SECRET_KEY = os.environ.get("S3_SECRET_KEY")
    
    GPT_APP_KEY = os.environ.get("GPT_APP_KEY")

    @property
    def get_db_url(self):
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PW}@{self.DB_HOST}:{self.DB_PORT}/dailyq' \
               f'?charset=utf8mb4'

    def get_exam_image_url(self, count: Optional[int] = None):
        if count is None:
            return f'https://{self.S3_BUCKET_NAME}.s3.{self.S3_REGION}.amazonaws.com/no_exam.png'
        else:
            return f'https://{self.S3_BUCKET_NAME}.s3.{self.S3_REGION}.amazonaws.com/exam_result_{count}.png'

    S3_CLIENT = boto3.client(
        's3',
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        region_name=S3_REGION
    )

setting = Setting()