from fastapi import APIRouter, Query, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from pytz import timezone
from typing import List

from app.core.auth import auth
from app.user.service import service
from app.user.dto.response import MonthlyExamResponse, DailyQuizResponse, DailyQuizResultResponse, MyPageResponse, UserSearchResponse
from app.user.dto.request import DailyQuizRequest

router = APIRouter(tags=['☑️ User : 유저 관련 API 모음'], prefix='/user')

@router.get(
    path='/monthly',
    summary='유저 월간 및 일별 문제풀이 조회',
    description='## ✔️️ [유저 월간 및 일별 문제풀이 조회] \n',
    response_model=MonthlyExamResponse
)
def get_user_info(
    date: str = Query(default=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d')),
    user_id=Depends(auth.auth_wrapper)
):
    region, monthly_exam, today_exam = service.get_user_monthly_and_daily_problem_solving(user_id, date)
    return MonthlyExamResponse(
        region=region,
        monthly_exam=monthly_exam,
        today_exam=today_exam
    )

@router.get(
    path='/quiz',
    summary='유저 데일리 퀴즈 문제 조회',
    description='## ✔️️ [유저 데일리 퀴즈 문제 조회] \n',
    response_model=DailyQuizResponse
)
def get_user_daily_quiz(
    date: str = Query(default=datetime.now(timezone('Asia/Seoul')).strftime('%Y-%m-%d')),
    user_id=Depends(auth.auth_wrapper)
):
    solved_index, questions = service.get_user_daily_quiz(date, user_id)
    return DailyQuizResponse(
        solved_index=solved_index,
        questions=questions
    )


@router.post(
    path='/quiz',
    summary='유저 데일리 퀴즈 문제 제출',
    description='## ✔️️ [유저 데일리 퀴즈 문제 제출] \n'
)
def post_user_daily_quiz(
    request: DailyQuizRequest,
    user_id=Depends(auth.auth_wrapper)
):
    service.update_user_daily_quiz(user_id, request.question_id, request.choose)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "정답 저장이 완료되었습니다."})


@router.get(
    path='/quiz/result',
    summary='유저 데일리 퀴즈 결과 조회',
    description='## ✔️️ [유저 데일리 퀴즈 결과 조회] \n',
    response_model=DailyQuizResultResponse
)
def get_user_daily_quiz_result(
    user_id=Depends(auth.auth_wrapper)
):
    correct_rate, comment, difficult, subject = service.get_user_daily_quiz_result(user_id)
    return DailyQuizResultResponse(
        correct_rate=correct_rate,
        comment=comment,
        difficult=difficult,
        subject=subject
    )

@router.get(
    path='',
    summary='유저 마이페이지 (분석 / 마이페이지 탭)',
    description='## ✔️️ [유저 마이페이지 (분석)] \n',
    response_model=MyPageResponse
)
def get_user_my_page(
    user_id=Depends(auth.auth_wrapper)
):
    (
        nickname, level, profile, created_date, levelup_info, total_question_count, total_date, 
        monthly_analysis, subject_analysis, difficult_analysis
    ) = service.get_user_my_page(user_id)

    return MyPageResponse(
        nickname=nickname,
        level=level,
        profile=profile,
        created_date=created_date,
        levelup_info=levelup_info,
        total_question_count=total_question_count,
        total_date=total_date,
        monthly_analysis=monthly_analysis,
        subject_analysis=subject_analysis,
        difficult_analysis=difficult_analysis
    )

@router.get(
    path='/search',
    summary='유저 검색 (채팅 탭)',
    description='## ✔️️ [유저 검색] \n'
                '### - 검색 키워드가 없으면 전체 유저 조회 \n'
                '### - 검색 키워드가 있으면 해당 키워드로 유저 검색 \n'
                '### - 유저 닉네임 가나다순으로 정렬',
    response_model=List[UserSearchResponse]
)
def get_user_search(
    keyword: str = Query(default=''),
    user_id=Depends(auth.auth_wrapper)
):
    return service.search_user(keyword, user_id)