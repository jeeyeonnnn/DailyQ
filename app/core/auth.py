from typing import Optional, Annotated

import jwt
import time
from fastapi import HTTPException, Header
from datetime import datetime, timedelta
from pytz import timezone

from app.core.model import User
from app.core.db import database
from app.core.setting import setting


class AuthHandler:
    @staticmethod
    def encode_token(user_id):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=30),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, setting.JWT_SECRET, algorithm=setting.JWT_ALGORITHM)


    @staticmethod
    def decode_token(token):
        try:
            payload = jwt.decode(token, setting.JWT_SECRET, algorithms=setting.JWT_ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:  # refresh token으로 access 재발급
            raise HTTPException(status_code=401, detail='비정상적인 접근입니다. 재로그인 해주세요 !')
        except jwt.InvalidTokenError as e:  # access token 오류
            raise HTTPException(status_code=401, detail='비정상적인 접근입니다. 재로그인 해주세요 !')

    def auth_wrapper(self, access_token: Annotated[str, Header()]):
        return self.decode_token(access_token[7:])  # Bearer 제거 


    def generate_apple_client_secret(self):
        headers = {
            "kid": setting.APPLE_KEY_ID,
            "alg": "ES256"
        }

        claims = {
            "iss": setting.APPLE_TEAM_ID,
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400 * 180,
            "aud": "https://appleid.apple.com",
            "sub": setting.APPLE_CLIENT_ID
        }

        with open('app/core/apple.p8', 'r') as f:
            private_key = f.read()

        client_secret = jwt.encode(
            payload=claims,
            key=private_key,
            algorithm="ES256",
            headers=headers
        )

        return client_secret
    
    def decode_id_token(self, id_token: str):
        decoded = jwt.decode(id_token, options={"verify_signature": False})
        return decoded


auth = AuthHandler()