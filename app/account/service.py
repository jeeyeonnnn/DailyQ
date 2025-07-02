import bcrypt
import requests

from app.account.dto.request import SignUpRequest, SignInRequest, OnboardingRequest, GoogleSignInRequest
from app.account.repository import repository
from app.core.auth import auth
from app.core.setting import setting

class AccountService:
    def sign_up(self, request: SignUpRequest):
        hash_password = bcrypt.hashpw(request.password.encode(encoding="utf-8"),
                                bcrypt.gensalt()).decode("utf-8")
        return repository.sign_up(request.user_id, hash_password)

    def sign_in(self, request: SignInRequest):
        return repository.sign_in(request.user_id, request.password)

    def onboarding(self, user_id: str, request: OnboardingRequest):
        return repository.onboarding(user_id, request.nickname, request.pet_type, request.region_id)


    def social_sign_in(self, login_type: str, user_key: str):
        return repository.social_sign_in(login_type, user_key)

    def resign(self, user_id: int):
        return repository.resign(user_id)

    def apple_sign_in(self, code: str):
        client_secret = auth.generate_apple_client_secret()
        print(f'client id : {setting.APPLE_CLIENT_ID}')
        data = {
            "client_id": setting.APPLE_CLIENT_ID,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
        }

        response = requests.post("https://appleid.apple.com/auth/token", data=data)
        print(f'response : {response.json()}')
        id_token = response.json()['id_token']
        decoded = auth.decode_id_token(id_token)
        return decoded['sub']

service = AccountService()