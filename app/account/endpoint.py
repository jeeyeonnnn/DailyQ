from fastapi import APIRouter
from fastapi import status, Depends
from fastapi.responses import JSONResponse

from app.account.dto.request import SignUpRequest, SignInRequest, OnboardingRequest, GoogleSignInRequest, AppleSignInRequest
from app.account.dto.response import SignInResponse
from app.account.service import service
from app.core.auth import auth

router = APIRouter(tags=['☑️ Account : 계정 관련 API 모음'], prefix='/account')

@router.post(
    path="/sign-up",
    summary="회원가입",
    description='## ✔️️ [회원 가입] \n'
                '### 🗨️ Status Code 400 Message \n'
                '- ID가 이미 존재하는 경우 \n'
                '''
                    {
                        "message": "이미 존재하는 아이디입니다."
                    }
                '''
)
def sign_up(request: SignUpRequest):
    status_code, user_idx = service.sign_up(request)
    
    if status_code == -1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "이미 존재하는 아이디입니다."})
    elif status_code == 0:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "message": "회원가입이 완료되었습니다.",
            "access_token": auth.encode_token(user_idx)
        })


@router.post(
    path="/sign-in",
    summary="로그인",
    description='## ✔️️ [로그인] \n'
                '### 🗨️ Response \n'
                'is_signup_done \n'
                '- True : 반려식 + 지역 모두 입력 후 모든 회원가입 절차를 완료한 경우 \n'
                '- False : 아이디 + 비번 계정 가입만 진행한 경우 (중간에 이탈) \n'
                '### 🗨️ Status Code 400 Message \n'
                '- ID가 존재하지 않거나 비밀번호가 틀린 경우 \n'
                '- 탈퇴한 유저 \n'
                '''
                    {
                        "message": "아이디 또는 비밀번호가 일치하지 않습니다."
                    }
                    
                    {
                        "message": "탈퇴한 유저입니다."
                    }
                ''',
    status_code=status.HTTP_201_CREATED,
    response_model=SignInResponse
)
def sign_in(request: SignInRequest):
    status_code, user_id, is_signup_done = service.sign_in(request)
    
    if status_code in [-1, -2]:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "아이디 또는 비밀번호가 일치하지 않습니다."})
    elif status_code == -3:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "탈퇴한 유저입니다."})
    elif status_code == 0:
        access_token = auth.encode_token(user_id)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={
            "message": "로그인이 완료되었습니다.", 
            "access_token": access_token,
            "is_signup_done": is_signup_done
        })


@router.post(
    path='/google-sign-in',
    summary='구글 로그인',
    description='## ✔️️ [구글 로그인 + 회원가입] \n',
    response_model=SignInResponse
)
def google_sign_in(request: GoogleSignInRequest):
    user_id, is_signup_done = service.social_sign_in('G', request.google_user_key)
    
    if user_id == -1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "탈퇴한 유저입니다."})
    
    access_token = auth.encode_token(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "message": "로그인이 완료되었습니다.", 
        "access_token": access_token,
        "is_signup_done": is_signup_done
    })
    
    
@router.post(
    path='/apple-sign-in',
    summary='애플 로그인',
    description='## ✔️️ [애플 로그인 + 회원가입] \n',
    response_model=SignInResponse
)
def apple_sign_in(request: AppleSignInRequest):
    print(f'code : {request.code}')
    apple_user_id = service.apple_sign_in(request.code)
    user_id, is_signup_done = service.social_sign_in('A', apple_user_id)
    
    if user_id == -1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "탈퇴한 유저입니다."})
    
    access_token = auth.encode_token(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "message": "로그인이 완료되었습니다.", 
        "access_token": access_token,
        "is_signup_done": is_signup_done
    })


@router.post(
    path='/resign',
    summary='회원탈퇴',
    description='## ✔️️ [회원탈퇴] \n'
                '### 🗨️ Status Code 400 Message \n'
                '- 회원탈퇴 처리 중 오류가 발생한 경우 \n'
                '''
                    {
                        "message": "회원탈퇴 처리 중 오류가 발생했습니다."
                    }
                '''
)
def resign(
    user_id=Depends(auth.auth_wrapper)
):
    service.resign(user_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "회원탈퇴가 완료되었습니다."})


@router.post(
    path='/onboarding',
    summary='온보딩 = 반려식 + 지역 저장',
    description='## ✔️️ [온보딩] \n'
                '### 🗨️ Response \n'
                '- pet_type = 나무(1) / 선인장(2) / 버섯(3) / 꽃(4) \n \n'
                '### 🗨️ Status Code 400 Message \n'
                '- 이미 존재하는 반려식입니다. \n'
                '''
                    {
                        "message": "이미 존재하는 반려식입니다."
                    }
                '''
)
def onboarding(
    request: OnboardingRequest,
    user_id=Depends(auth.auth_wrapper)
):  
    status_code = service.onboarding(user_id, request)
    
    if status_code == -1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "이미 존재하는 반려식입니다."})
    elif status_code == -2:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "이미 온보딩 완료되었습니다."})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "온보딩이 완료되었습니다."})