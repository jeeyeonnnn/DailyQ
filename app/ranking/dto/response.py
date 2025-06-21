from pydantic import BaseModel, json_schema

from app.ranking.dto.service import Ranking


class RankingResponse(BaseModel):
    region: str
    user_ranking: Ranking
    ranking_info: list[Ranking]

    class Config:
        json_schema_extra = {
            'example': {
                "region": "남양주시",
                "user_ranking": {
                    "ranking": 2,
                    "nickname": "무지개쿵야",
                    "level": 1,
                    "profile": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/ranking_1.png",
                    "question_count": 20,
                    "correct_rate": 65
                },
                "ranking_info": [
                    {
                    "ranking": 1,
                    "nickname": "꽃붕이",
                    "level": 1,
                    "profile": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/ranking_1.png",
                    "question_count": 10,
                    "correct_rate": 90
                    },
                    {
                    "ranking": 2,
                    "nickname": "무지개쿵야",
                    "level": 1,
                    "profile": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/ranking_1.png",
                    "question_count": 20,
                    "correct_rate": 65
                    }
                ]
            }
        }