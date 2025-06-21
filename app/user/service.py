from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
from collections import defaultdict
from pytz import timezone

from app.user.repository import repository
from app.user.dto.service import (
    MonthlyExam, ExamInfo, TodayExamInfo, DailyExamInfo, QuestionInfo, SubjectResult, DifficultResult, LevelUpInfo, 
    SubjectAnalysis, DifficultAnalysis
)
from app.core.setting import setting

class UserService:
    def get_user_monthly_and_daily_problem_solving(self, user_id: int, today: str):
        monthly_exam, region = [], repository.get_region(user_id)
        first_date = datetime.strptime(today, '%Y-%m-%d').replace(day=1)
        last_date = first_date + relativedelta(months=1) - timedelta(days=1)
        monthly_exam_data = repository.get_monthly_exam_data(user_id, first_date, last_date)

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

        is_exit_data = repository.is_exist_exam_today(user_id, today)
        if is_exit_data:
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
            ) if is_exit_data else None,
            incorrect=DailyExamInfo(
                count=len(incorrect_exam),
                questions=incorrect_exam
            ) if is_exit_data else None
        )

    def get_user_daily_quiz(self, date: str, user_id: int):
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

    def random_choose_quiz(self, user_id: int, date: str, daily_quiz: list):
        selected_questions, question_count = [], 10
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

    
    def update_user_daily_quiz(self, user_id: int, question_id: int, choose: int):
        repository.update_exam_choose(user_id, question_id, choose)

    def get_user_daily_quiz_result(self, user_id: int):
        self.check_user_level_up(user_id)
        current_date = repository.get_current_date(user_id)
        correct_rate, difficult, subject = repository.get_user_daily_quiz_result(user_id, current_date)
        subject_result, difficult_result = [], []

        for diff in difficult:
            difficult_result.append(
                DifficultResult(
                    name=diff.name,
                    total=diff.total,
                    correct=diff.correct
                )
            )
        
        for sub in subject:
            subject_result.append(
                SubjectResult(
                    name=sub.name,
                    total=sub.total,
                    correct=sub.correct
                )
            )
        return int(correct_rate), self.get_comment_by_correct_rate(correct_rate), difficult_result, subject_result

    def check_user_level_up(self, user_id: int):
        level, total_question_count = repository.get_user_level_and_total_question_count(user_id)
        
        if level == 1 and total_question_count >= 30:
            repository.update_user_level(user_id, 2)
        elif level == 2 and total_question_count >= 100:
            repository.update_user_level(user_id, 3)
        elif level == 3 and total_question_count >= 300:
            repository.update_user_level(user_id, 4)
        elif level == 4 and total_question_count >= 500:
            repository.update_user_level(user_id, 5)
    
    def get_comment_by_correct_rate(self, correct_rate: float):
        comment = {
            1: [
                "완벽한 결과예요! 이 부분은 정말 자신 있어도 되겠어요 👏",
                "매우 훌륭해요! 이 주제는 이미 충분히 잘 알고 있네요 💯",
                "거의 실수가 없어요. 안정적인 실력이 느껴집니다!"
            ],
            2: [
                "좋은 흐름이에요! 조금 더 정리하면 완벽해질 수 있어요 👍",
                "잘 하고 있어요! 틀린 문제를 다시 한번 살펴보면 더 좋아질 거예요",
                "이 정도면 충분히 잘 해냈어요. 한두 부분만 더 확실히 해두면 좋겠어요 😊"
            ],
            3: [
                "가능성이 보여요! 이해한 부분과 헷갈렸던 부분을 구분해보면 더 나아질 거예요 🔍",
                "절반 이상 해냈다는 건 좋은 출발이에요. 약했던 문제들을 하나씩 다시 생각해보면 돼요!",
                "중간 정도의 결과지만, 개선할 여지가 충분히 보여요. 방향은 맞고 있어요!"
            ],
            4: [
                "조금 더 연습이 필요해요. 개념을 다시 차근차근 정리해보면 좋아질 거예요 📘",
                "이번에는 어렵게 느껴졌을 수 있어요. 중요한 포인트만 다시 확인해보는 걸 추천해요!",
                "결과는 아쉽지만, 지금부터 시작해도 충분히 따라잡을 수 있어요. 포기하지 마세요 💪"
            ]
        }

        idx = random.randint(0, 2)
        key = 1 if correct_rate >= 90 else 2 if correct_rate >= 70 else 3 if correct_rate >= 40 else 4
        return comment[key][idx]

    def get_user_my_page(self, user_id: int):
        user_info, total_question_count, total_date = repository.get_user_info(user_id)
        levelup_info = self.get_levelup_info(user_info.level, total_question_count)

        pre_correct_rate, current_correct_rate = self.analyisis_correct_rate_mom(user_id)
        subject_analysis = self.analyisis_subject_analysis(user_id)
        difficult_analysis = self.analyisis_difficult_analysis(user_id)

        return (
            user_info.name,
            user_info.level,
            f'https://{setting.S3_BUCKET_NAME}.s3.{setting.S3_REGION}.amazonaws.com/{user_info.profile}',
            user_info.created_at.date().strftime('%Y-%m-%d'),
            levelup_info,
            total_question_count,
            total_date,
            pre_correct_rate,
            current_correct_rate,
            subject_analysis,
            difficult_analysis
        )

    def analyisis_subject_analysis(self, user_id: int):
        subject_analysis = []
        for subject_info in repository.get_subject_analysis(user_id):
            total_rate = round(subject_info.total_correct / subject_info.total * 100, 0) if subject_info.total > 0 else 0
            user_rate = round(subject_info.user_correct / subject_info.user * 100, 0) if subject_info.user > 0 else 0
            subject_analysis.append(
                SubjectAnalysis(
                    subject=subject_info.name,
                    total=total_rate,
                    user=user_rate
                )
            )
        return subject_analysis

    def analyisis_difficult_analysis(self, user_id: int):
        difficult_analysis = []
        for difficult_info in repository.get_difficult_analysis(user_id):
            total_rate = round(difficult_info.total_correct / difficult_info.total * 100, 0) if difficult_info.total > 0 else 0
            user_rate = round(difficult_info.user_correct / difficult_info.user * 100, 0) if difficult_info.user > 0 else 0
            difficult_analysis.append(
                DifficultAnalysis(
                    difficult=difficult_info.name,
                    total=total_rate,
                    user=user_rate
                )
            )
        return difficult_analysis

    def analyisis_correct_rate_mom(self, user_id: int):
        today = datetime.now(timezone('Asia/Seoul'))
        current_month_first = today.replace(day=1)
        pre_month_last = current_month_first - timedelta(days=1)
        pre_month_first = pre_month_last.replace(day=1)

        pre_correct_rate = repository.get_correct_rate_by_date(user_id, pre_month_first, pre_month_last)
        current_correct_rate = repository.get_correct_rate_by_date(user_id, current_month_first, today)
        return pre_correct_rate, current_correct_rate

    def get_levelup_info(self, level: int, question_count: int):
        if level == 1:
            total, left = 30, 30 - question_count
        elif level == 2:
            total, left = 100, 100 - question_count
        elif level == 3:
            total, left = 300, 300 - question_count
        elif level == 4:
            total, left = 500, 500 - question_count

        return LevelUpInfo(
            current=question_count,
            left=left,
            total=total
        )
service = UserService()