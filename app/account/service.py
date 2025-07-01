import bcrypt

from app.account.dto.request import SignUpRequest, SignInRequest, OnboardingRequest, GoogleSignInRequest
from app.account.repository import repository

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

service = AccountService()