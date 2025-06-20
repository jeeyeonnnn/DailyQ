from datetime import datetime

from app.user.repository import repository
from app.user.dto.service import MonthlyExam, ExamInfo, TodayExamInfo, DailyExamInfo
from app.core.setting import setting

class UserService:
    def get_user_monthly_and_daily_problem_solving(self, user_id: str, today: str):
        monthly_exam = []
        first_date = datetime.strptime(today, '%Y-%m-%d').replace(day=1)
        monthly_exam_data = repository.get_monthly_exam_data(user_id, first_date, datetime.strptime(today, '%Y-%m-%d'))

        for date, correct_count in monthly_exam_data:
            if correct_count is not None:
                if correct_count <= 3:
                    correct_count = 1
                elif correct_count <= 6:
                    correct_count = 2
                elif correct_count <= 8:
                    correct_count = 3
                else:
                    correct_count = 4

            monthly_exam.append(
                MonthlyExam(
                    date=date,
                    image=setting.get_exam_image_url(correct_count)
                )
            )

        if monthly_exam_data[-1][1] is not None:
            correct, incorrect = repository.get_daily_exam_data(user_id, today)
            correct_exam, incorrect_exam = [], []

            for question in correct:
                correct_exam.append(
                    ExamInfo(
                        subject=question.subject,
                        difficult=question.difficult,
                        question=question.name,
                        select_1=question.select_1,
                        select_2=question.select_2,
                        select_3=question.select_3,
                        select_4=question.select_4,
                        answer=question.answer,
                        user_select=question.choose,
                        explanation=question.explanation
                    )
                )

            for question in incorrect:
                incorrect_exam.append(
                    ExamInfo(
                        subject=question.subject,
                        difficult=question.difficult,
                        question=question.name,
                        select_1=question.select_1,
                        select_2=question.select_2,
                        select_3=question.select_3,
                        select_4=question.select_4,
                        answer=question.answer,
                        user_select=question.choose,
                        explanation=question.explanation
                    )
                )
        return monthly_exam, TodayExamInfo(
            correct=DailyExamInfo(
                count=len(correct_exam),
                questions=correct_exam
            ) if monthly_exam_data[-1][1] is not None else None,
            incorrect=DailyExamInfo(
                count=len(incorrect_exam),
                questions=incorrect_exam
            ) if monthly_exam_data[-1][1] is not None else None
        )


service = UserService()