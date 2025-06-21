from datetime import datetime
import random
from collections import defaultdict

from app.user.repository import repository
from app.user.dto.service import MonthlyExam, ExamInfo, TodayExamInfo, DailyExamInfo, QuestionInfo
from app.core.setting import setting

class UserService:
    def get_user_monthly_and_daily_problem_solving(self, user_id: str, today: str):
        monthly_exam, region = [], repository.get_region(user_id)
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
        return region, monthly_exam, TodayExamInfo(
            correct=DailyExamInfo(
                count=len(correct_exam),
                questions=correct_exam
            ) if monthly_exam_data[-1][1] is not None else None,
            incorrect=DailyExamInfo(
                count=len(incorrect_exam),
                questions=incorrect_exam
            ) if monthly_exam_data[-1][1] is not None else None
        )

    def get_user_daily_quiz(self, date: str, user_id: str):
        is_exit, daily_quiz = repository.get_daily_quiz(date, user_id)
        solved_index, questions = 100, []

        if not is_exit:
            daily_quiz = self.random_choose_quiz(user_id, date, daily_quiz)
        
        for index, question in enumerate(daily_quiz):
            questions.append(
                QuestionInfo(
                    subject=question.subject,
                    difficult=question.difficult,
                    question_id=question.id,
                    question=question.name,
                    select_1=question.select_1,
                    select_2=question.select_2,
                    select_3=question.select_3,
                    select_4=question.select_4,
                    answer=question.answer,
                    explanation=question.explanation,
                    correct_rate=random.randint(67, 98)
                )
            )
            solved_index = solved_index if question.choose is not None else min(solved_index, index)

        return solved_index, questions

    def random_choose_quiz(self, user_id: str, date: str, daily_quiz: list):
        selected_questions, question_count = [], random.randint(10, 15)
        subject_groups = defaultdict(list)
        difficult_groups = defaultdict(list)

        # Step 1: 그룹화
        for q in daily_quiz:
            subject_groups[q.subject].append(q)
            difficult_groups[q.difficult].append(q)

        # Step 2: 각 Subject에서 2문제씩 뽑기
        for questions in subject_groups.values():
            sampled = random.sample(questions, min(2, len(questions)))
            selected_questions.extend(sampled)

        # Step 3: 각 Difficult에서 최소 1문제씩 존재하는지 확인하고, 없으면 추가
        for diff, questions in difficult_groups.items():
            if not any(q in selected_questions for q in questions):
                selected_questions.append(random.choice(questions))

        # Step 4: 중복 제거 및 랜덤 셔플
        unique_questions = {q.id: q for q in selected_questions}.values()
        final_questions = list(unique_questions)

        # 부족하면 추가 채우기
        remaining = [q for q in daily_quiz if q.id not in [fq.id for fq in final_questions]]
        random.shuffle(remaining)
        while len(final_questions) < question_count and remaining:
            final_questions.append(remaining.pop())

        # 최종 섞기
        random.shuffle(final_questions)
        repository.update_exam(user_id, date, [q.id for q in final_questions[:question_count]])
        return final_questions[:question_count]

    
    def update_user_daily_quiz(self, user_id: str, question_id: int, choose: int):
        repository.update_exam_choose(user_id, question_id, choose)

    def get_user_daily_quiz_result(self, user_id: str):
        correct_rate, tag, difficult = repository.get_user_daily_quiz_result(user_id)

service = UserService()