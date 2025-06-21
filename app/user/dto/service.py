from pydantic import BaseModel
from typing import List, Optional

class MonthlyExam(BaseModel):
    date: str
    image: str


class ExamInfo(BaseModel):
    subject: str
    difficult: str
    question: str
    select_1: str
    select_2: str
    select_3: str
    select_4: str
    answer: int
    user_select: int
    explanation: str
    

class DailyExamInfo(BaseModel):
    count: int
    questions: List[ExamInfo]

class TodayExamInfo(BaseModel):
    correct: Optional[DailyExamInfo] = None
    incorrect: Optional[DailyExamInfo] = None


class QuestionInfo(BaseModel):
    subject: str
    difficult: str
    question_id: int
    question: str
    select_1: str
    select_2: str
    select_3: str
    select_4: str
    answer: int
    explanation: str
    correct_rate: int


class SubjectResult(BaseModel):
    name: str
    total: int
    correct: int


class DifficultResult(BaseModel):
    name: str
    total: int
    correct: int