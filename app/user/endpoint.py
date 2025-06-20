from fastapi import APIRouter, Query, Depends
from datetime import datetime
from pytz import timezone

from app.core.auth import auth
from app.user.service import service
from app.user.dto.response import MonthlyExamResponse

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
    monthly_exam, today_exam = service.get_user_monthly_and_daily_problem_solving(user_id, date)
    return MonthlyExamResponse(
        monthly_exam=monthly_exam,
        today_exam=today_exam
    )