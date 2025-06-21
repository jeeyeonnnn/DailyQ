from fastapi import APIRouter, Depends

from app.core.auth import auth
from app.ranking.dto.response import RankingResponse
from app.ranking.service import service

router = APIRouter(prefix='/ranking', tags=['ranking'])

@router.get(
    path='',
    summary='랭킹 조회',
    description='## ✔️️ [랭킹 조회] \n'
                '### ⭐️ 만약, 해당 주에 1문제도 풀지 않았다면 ranking은 "-"로 표시됩니다.'
    '''
        "user_ranking": {
            "ranking": "-",
            "nickname": "나는멋쟁이",
            "level": 1,
            "profile": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/ranking_1.png",
            "question_count": 0,
            "correct_rate": 0
        }
    ''',
    response_model=RankingResponse
)
def get_ranking(
    user_id=Depends(auth.auth_wrapper)
):
    region, user_ranking, ranking_info = service.get_ranking(user_id)
    return RankingResponse(
        region=region,
        user_ranking=user_ranking,
        ranking_info=ranking_info
    )