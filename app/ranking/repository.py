from datetime import datetime, timedelta

from sqlalchemy import func, case, alias, and_, literal

from app.core.db import database
from app.core.model import Region, User, Exam, Profile


class RankingRepository:
    def get_ranking(self, user_id: int, monday: datetime, today: datetime):
        today = today + timedelta(days=1)
        with database.session_factory() as db:
            region, region_id = db.query(
                Region.sub,
                Region.id
            ).join(User, User.region_id == Region.id)\
                .filter(User.id == user_id).one()

            correct_expr = (
                func.round(
                    func.sum(
                        case((Exam.is_correct == 1, 1), else_=0)
                    ) / func.nullif(func.count(Exam.order), 0) * 100,
                    1
                )
            )

            # 전체 랭킹 쿼리 (서브쿼리화)
            ranking_subquery = db.query(
                func.row_number().over(order_by=[
                    func.count().desc(),
                    correct_expr.desc()
                ]).label('ranking'),
                User.id.label('user_id'),
                User.name,
                User.level,
                User.pet_type,
                Profile.ranking.label('profile'),
                correct_expr.label('correct_rate'),
                func.count().label('question_count')
            ).select_from(Exam)\
            .join(User, User.id == Exam.user_id)\
            .join(Profile, and_(
                Profile.pet_type == User.pet_type,
                Profile.level == User.level
            ))\
            .filter(
                User.region_id == region_id,
                User.is_resigned == 0,
                Exam.created_date >= monday.strftime('%Y-%m-%d'),
                Exam.created_date < today.strftime('%Y-%m-%d')
            ).group_by(User.id, User.name, User.level, User.pet_type, Profile.ranking)\
            .subquery()
            

            Ranking = alias(ranking_subquery)
            # 전체 랭킹 top 10
            top_10 = db.query(Ranking).order_by(Ranking.c.question_count.desc(), Ranking.c.correct_rate.desc()).limit(10).all()

            # 현재 유저의 랭킹
            user_ranking = db.query(Ranking).filter(Ranking.c.user_id == user_id).first()

            if user_ranking is None:
                user_ranking = db.query(
                    literal('-').label('ranking'),
                    User.name,
                    User.level,
                    Profile.ranking.label('profile'),
                    literal(0).label('question_count'),
                    literal(0).label('correct_rate')
                ).join(Profile, and_(
                    Profile.pet_type == User.pet_type,
                    Profile.level == User.level
                )).filter(User.id == user_id).one()

            return region, user_ranking, top_10

            

repository = RankingRepository()
