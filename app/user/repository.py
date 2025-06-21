from datetime import datetime, timedelta
from sqlalchemy import and_

from app.core.db import database
from app.core.model import Exam, Question, Subject, Difficult, Region, User

class UserRepository:
    def get_monthly_exam_data(self, user_id: str, first_date: datetime, today: datetime):
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
    
    def get_daily_exam_data(self, user_id: str, today: str):
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


    def get_daily_quiz(self, date: str, user_id: str):
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
    
    def update_exam(self, user_id: str, date: str, question_id_list: list):
        with database.session_factory() as db:
            for index, question_id in enumerate(question_id_list):
                db.add(Exam(user_id=user_id, question_id=question_id, created_date=date, order=index+1))
            db.commit()

    def update_exam_choose(self, user_id: str, question_id: int, choose: int):
        with database.session_factory() as db:
            question = db.query(Question).filter(Question.id == question_id).one()
            exam = db.query(Exam).filter(Exam.user_id == user_id, Exam.question_id == question_id).one()
            exam.choose = choose
            exam.is_correct = 1 if choose == question.answer else 0
            db.commit()

    def get_region(self, user_id: str):
        with database.session_factory() as db:
            return db.query(Region)\
                .join(User, User.region_id == Region.id)\
                    .filter(User.id == user_id).one().sub

    def get_user_daily_quiz_result(self, user_id: str):
        with database.session_factory() as db:
            exam = db.query(
                Subject.id,
                Subject.name,
                Difficult.id,
                Difficult.name,
                Exam.is_correct
            ).join(Question, Question.id == Exam.question_id)\
            .join(Subject, Subject.id == Question.subject_id)\
            .join(Difficult, Difficult.id == Question.difficult_id)\
            .filter(Exam.user_id == user_id, Exam.created_date == '2025-06-20')

            correct, incorrect = exam.filter(Exam.is_correct == 1).count(), exam.filter(Exam.is_correct == 0).count()

            correct_rate = round(correct / (correct + incorrect) * 100, 2)
            



repository = UserRepository()