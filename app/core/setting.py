import os
from dotenv import load_dotenv

load_dotenv("./app/core/.env")


class Setting:
    DB_USER = os.environ.get("DB_USER")
    DB_PW = os.environ.get("DB_PW")
    DB_PORT = os.environ.get("DB_PORT")
    DB_HOST = os.environ.get("DB_HOST")
    
    @property
    def get_db_url(self):
        return f'mysql+pymysql://{self.DB_USER}:{self.DB_PW}@{self.DB_HOST}:{self.DB_PORT}/dailyq' \
               f'?charset=utf8'

setting = Setting()