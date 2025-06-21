from datetime import datetime, timedelta
from sqlalchemy import and_, func, distinct
from sqlalchemy.sql import func, case

from app.core.db import database
from app.core.model import Exam, Question, Subject, Difficult, Region, User, Profile

class UserRepository:
    def get_monthly_exam_data(self, user_id: int, first_date: datetime, today: datetime):
        monthly_exam_data = []
        date_list = [
            (first_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((today - first_date).days + 1)
        ]
        with database.session_factory() as db:
            for date in date_list:
                exam = db.query(Exam).filter(Exam.user_id == user_id, Exam.created_date == date, Exam.choose != None)

                monthly_exam_data.append(
                    (
                        date,
                        None if exam.count() < 10 else exam.filter(Exam.is_correct == 1).count()
                    )
                )
        return monthly_exam_data
    
    def get_daily_exam_data(self, user_id: int, today: str):
        with database.session_factory() as db:
            exam = db.query(
                Subject.name.label('subject'),
                Difficult.name.label('difficult'),
                Question.id,
                Question.name,
                Question.select_1,
                Question.select_2,
                Question.select_3,
                Question.select_4,
                Question.answer,
                Question.explanation,
                Exam.choose,
                Exam.is_correct
            ).join(Exam, Exam.question_id == Question.id)\
                .join(Subject, Subject.id == Question.subject_id)\
                .join(Difficult, Difficult.id == Question.difficult_id)\
                .filter(Exam.user_id == user_id, Exam.created_date == today)
            
            return exam.filter(Exam.is_correct == 1).all(), exam.filter(Exam.is_correct == 0).all()


    def get_daily_quiz(self, date: str, user_id: int):
        with database.session_factory() as db:
            # 오늘 퀴즈를 푼 이력이 있을 경우
            if db.query(Exam).filter(Exam.user_id == user_id, Exam.created_date == date).count() > 0:
                quiz_list = db.query(
                    Subject.name.label('subject'),
                    Difficult.name.label('difficult'),
                    Exam.choose,
                    Question.id,
                    Question.name,
                    Question.select_1,
                    Question.select_2,
                    Question.select_3,
                    Question.select_4,
                    Question.answer,
                    Question.explanation
                ).join(Question, Question.id == Exam.question_id)\
                .join(Subject, Subject.id == Question.subject_id)\
                .join(Difficult, Difficult.id == Question.difficult_id)\
                .filter(Exam.user_id == user_id, Exam.created_date == date)\
                .order_by(Exam.order).all()
                return True, quiz_list
        
            # 오늘 퀴즈를 푼 이력이 없을 경우
            quiz_list = db.query(
                Subject.name.label('subject'),
                Difficult.name.label('difficult'),
                Exam.choose,
                Question.id,
                Question.name,
                Question.select_1,
                Question.select_2,
                Question.select_3,
                Question.select_4,
                Question.answer,
                Question.explanation
            ).join(Subject, Subject.id == Question.subject_id)\
            .join(Difficult, Difficult.id == Question.difficult_id)\
            .outerjoin(Exam, and_(Exam.question_id == Question.id, Exam.user_id == user_id))\
            .filter(Exam.choose== None)\
            .all()
            return False, quiz_list
    
    def update_exam(self, user_id: int, date: str, question_id_list: list):
        with database.session_factory() as db:
            for index, question_id in enumerate(question_id_list):
                db.add(Exam(user_id=user_id, question_id=question_id, created_date=date, order=index+1))
            db.commit()

    def update_exam_choose(self, user_id: int, question_id: int, choose: int):
        with database.session_factory() as db:
            question = db.query(Question).filter(Question.id == question_id).one()
            exam = db.query(Exam).filter(Exam.user_id == user_id, Exam.question_id == question_id).one()
            exam.choose = choose
            exam.is_correct = 1 if choose == question.answer else 0
            db.commit()

    def get_region(self, user_id: int):
        with database.session_factory() as db:
            return db.query(Region)\
                .join(User, User.region_id == Region.id)\
                    .filter(User.id == user_id).one().sub

    def get_user_daily_quiz_result(self, user_id: int, date: str):
        with database.session_factory() as db:
            exam = db.query(Exam).filter(Exam.user_id == user_id, Exam.created_date == date)
            correct, incorrect = exam.filter(Exam.is_correct == 1).count(), exam.filter(Exam.is_correct == 0).count()
            correct_rate = round(correct / (correct + incorrect) * 100, 2) if correct + incorrect > 0 else 0

            # 난이도별 정답/오답 수
            difficult = db.query(
                Difficult.name,
                func.sum(
                    case(
                        (Exam.is_correct == 1, 1), 
                        else_=0
                    )
                ).label('correct'),
                func.sum(1).label('total')
            ).join(Question, Question.id == Exam.question_id)\
            .join(Difficult, Difficult.id == Question.difficult_id)\
            .filter(
                Exam.user_id == user_id,
                Exam.created_date == date
            ).group_by(Difficult.id).order_by(Difficult.id).all()

            # 주제별 정답/오답 수
            subject = db.query(
                Subject.name,
                func.sum(
                    case(
                        (Exam.is_correct == 1, 1), 
                        else_=0
                    )
                ).label('correct'),
                func.sum(1).label('total')
            ).join(Question, Question.id == Exam.question_id)\
            .join(Subject, Subject.id == Question.subject_id)\
            .filter(
                Exam.user_id == user_id,
                Exam.created_date == date
            ).group_by(Subject.id).order_by(Subject.id).all()

            return correct_rate, difficult, subject

    def get_current_date(self, user_id: int):
        with database.session_factory() as db:
            date_info = db.query(
                Exam.created_date,
                func.sum(
                    case(
                        (Exam.choose != None, 1), 
                        else_=0
                    )
                ).label('exam'),
                func.sum(1).label('total')
            ).filter(Exam.user_id == user_id).group_by(Exam.created_date)\
                .order_by(Exam.created_date.desc()).all()

        for date in date_info:
            if date.exam == date.total:
                return date.created_date
        return date_info[-1].created_date

    def is_exist_exam_today(self, user_id: int, today: str):
        with database.session_factory() as db:
            return True if db.query(Exam)\
                .filter(Exam.user_id == user_id, Exam.created_date == today)\
                    .count() > 0 else False
    
    def get_user_level_and_total_question_count(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                User.level,
                func.count().label('total_question_count')
            ).select_from(Exam).join(User, User.id == Exam.user_id)\
                .filter(User.id == user_id)\
                .group_by(User.level).one()

    def update_user_level(self, user_id: int, level: int):
        with database.session_factory() as db:
            user = db.query(User).filter(User.id == user_id).one()
            user.level = level
            db.commit()

    def get_user_info(self, user_id: int):
        with database.session_factory() as db:
            total_question_count = db.query(Exam).filter(Exam.user_id == user_id).count()
            total_date = db.query(distinct(Exam.created_date)).filter(Exam.user_id == user_id).count()
            return db.query(
                User.name,
                User.level,
                Profile.mypage.label('profile'),
                User.created_at
            ).join(Profile, and_(
                Profile.pet_type == User.pet_type,
                Profile.level == User.level
            )).filter(User.id == user_id).one(), total_question_count, total_date

    def get_correct_rate_by_date(self, user_id: int, first_date: datetime, last_date: datetime):
        with database.session_factory() as db:
            total, correct = db.query(
                func.count().label('total'),
                func.sum(
                    case(
                        (Exam.is_correct == 1, 1),
                        else_=0
                    )
                ).label('correct')
            ).select_from(Exam)\
            .filter(
                Exam.created_date >= first_date,
                Exam.created_date <= last_date,
                Exam.user_id == user_id
            ).one()

            return round(correct / total * 100, 0) if total > 0 else 0


    def get_subject_analysis(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                Subject.name,
                func.count().label('total'),
                func.sum(
                    case(
                        (Exam.is_correct == 1, 1),
                        else_=0
                    )
                ).label('total_correct'),
                func.sum(
                    case(
                        (Exam.user_id == user_id, 1),
                        else_=0
                    )
                ).label('user'),
                func.sum(
                    case(
                        (and_(
                            Exam.user_id == user_id,
                            Exam.is_correct == 1
                        ), 1),
                        else_=0
                    )
                ).label('user_correct')
            ).join(Question, Question.id == Exam.question_id)\
                .join(Subject, Subject.id == Question.subject_id)\
                .group_by(Subject.id).order_by(Subject.id).all()

    def get_difficult_analysis(self, user_id: int):
        with database.session_factory() as db:
            return db.query(
                Difficult.name,
                func.count().label('total'),
                func.sum(
                    case(
                        (Exam.is_correct == 1, 1),
                        else_=0
                    )
                ).label('total_correct'),
                func.sum(
                    case(
                        (Exam.user_id == user_id, 1),
                        else_=0
                    )
                ).label('user'),
                func.sum(
                    case(
                        (and_(
                            Exam.user_id == user_id,
                            Exam.is_correct == 1
                        ), 1),
                        else_=0
                    )
                ).label('user_correct')
            ).join(Question, Question.id == Exam.question_id)\
                .join(Difficult, Difficult.id == Question.difficult_id)\
                .group_by(Difficult.id).order_by(Difficult.id).all()

repository = UserRepository()