import bcrypt
from datetime import datetime
from pytz import timezone

from app.account.dto.request import SignUpRequest
from app.core.db import database
from app.core.model import User


class AccountRepository:
    def sign_up(self, user_id: str, password: str):
        with database.session_factory() as db:
            if db.query(User).filter(User.user_id == user_id).count() > 0:
                return -1, None  # 이미 존재하는 아이디
            
            now = datetime.now(timezone('Asia/Seoul'))
            db.add(User(user_id=user_id, password=password, created_at=now))
            db.commit()

            user_idx = db.query(User).filter(User.user_id == user_id).one().id
            return 0, user_idx  # 회원가입 성공

    def sign_in(self, user_id: str, password: str):
        with database.session_factory() as db:
            user = db.query(User).filter(User.user_id == user_id).first()
            if user is None:
                return -1, None, None  # 존재하지 않는 아이디
            if not bcrypt.checkpw(password.encode(encoding="utf-8"), user.password.encode(encoding="utf-8")):
                return -2, None, None  # 비밀번호 불일치
            
            is_sign_in_done = True if user.name is not None else False
            return 0, user.id, is_sign_in_done

    def onboarding(self, user_id: str, nickname: str, pet_type: int, region_id: int):
        with database.session_factory() as db:
            if db.query(User).filter(User.name == nickname).count() > 0:
                return -1  # 이미 존재하는 닉네임

            user: User = db.query(User).filter(User.id == user_id).one()

            if user.name is not None:
                return -2  # 이미 온보딩 완료
            
            user.name = nickname
            user.pet_type = pet_type
            user.region_id = region_id
            db.commit()
            return 0  # 온보딩 성공
    
    def google_sign_in(self, google_user_key: str):
        with database.session_factory() as db:
            user_id = f'G{google_user_key}'
            user = db.query(User).filter(User.user_id == user_id).first()

            if user is None:
                db.add(User(user_id=user_id, created_at=datetime.now(timezone('Asia/Seoul'))))
                db.commit()
                
                user_idx = db.query(User).filter(User.user_id == user_id).one().id
                return user_idx, False
            
            is_sign_in_done = True if user.name is not None else False
            return user.id, is_sign_in_done

repository = AccountRepository()