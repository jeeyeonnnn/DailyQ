from datetime import datetime, timedelta
from pytz import timezone

from app.ranking.repository import repository
from app.ranking.dto.service import Ranking
from app.core.setting import setting


class RankingService:
    def get_ranking(self, user_id: int):
        today = datetime.now(timezone('Asia/Seoul'))
        monday = today - timedelta(days=today.weekday())
        ranking_info = []
        region, user_ranking, all_ranking = repository.get_ranking(user_id, monday, today)

        user_ranking = Ranking(
            ranking=user_ranking.ranking,
            nickname=user_ranking.name,
            level=user_ranking.level,
            profile=f'https://{setting.S3_BUCKET_NAME}.s3.{setting.S3_REGION}.amazonaws.com/{user_ranking.profile}',
            question_count=user_ranking.question_count,
            correct_rate=user_ranking.correct_rate
        )

        for rank in all_ranking:
            ranking_info.append(
                Ranking(
                    ranking=rank.ranking,
                    nickname=rank.name,
                    level=rank.level,
                    profile=f'https://{setting.S3_BUCKET_NAME}.s3.{setting.S3_REGION}.amazonaws.com/{rank.profile}',
                    question_count=rank.question_count,
                    correct_rate=rank.correct_rate
                )
            )

        return region, user_ranking, ranking_info
        
service = RankingService()