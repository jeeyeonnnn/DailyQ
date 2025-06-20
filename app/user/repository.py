from datetime import datetime, timedelta

from app.core.db import database
from app.core.model import Exam, Question, Subject, Difficult

class UserRepository:
    def get_monthly_exam_data(self, user_id: str, first_date: datetime, today: datetime):
        monthly_exam_data = []
        date_list = [
            (first_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((today - first_date).days + 1)
        ]
        with database.session_factory() as db:
            for date in date_list:
                exam = db.query(Exam).filter(Exam.user_id == user_id, Exam.created_date == date)

                monthly_exam_data.append(
                    (
                        date,
                        None if exam.count() == 0 else exam.filter(Exam.is_correct == 1).count()
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
                .filter(Exam.user_id == user_id, Exam.created_date == today)\
                .order_by(Question.id)
            
            return exam.filter(Exam.is_correct == 1).all(), exam.filter(Exam.is_correct == 0).all()

    def delete_exam(self):
        with database.session_factory() as db:
            db.query(Exam).delete()
            db.commit()

repository = UserRepository()