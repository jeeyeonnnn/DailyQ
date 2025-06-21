from typing import List
from pydantic import BaseModel, json_schema

from app.user.dto.service import MonthlyExam, TodayExamInfo, QuestionInfo


class MonthlyExamResponse(BaseModel):
    region: str
    monthly_exam: List[MonthlyExam]
    today_exam: TodayExamInfo

    class Config:
        json_schema_extra = {
            "example": {
                "region": "남양주시",
                "monthly_exam": [
                    {
                    "date": "2025-06-01",
                    "image": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/no_exam.png"
                    },
                    {
                    "date": "2025-06-02",
                    "image": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/no_exam.png"
                    },
                    {
                    "date": "2025-06-03",
                    "image": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/no_exam.png"
                    },
                    {
                    "date": "2025-06-04",
                    "image": "https://daily-quizz.s3.ap-northeast-2.amazonaws.com/no_exam.png"
                    }
                ],
                "today_exam": {
                    "correct": {
                    "count": 7,
                    "questions": [
                        {
                        "subject": "수/과학",
                        "difficult": "중상",
                        "question": "E=mc²에서 c는 무엇을 의미하나요?",
                        "select_1": "에너지",
                        "select_2": "시간",
                        "select_3": "질량",
                        "select_4": "빛의 속도",
                        "answer": 4,
                        "user_select": 4,
                        "explanation": "아인슈타인의 방정식에서 c는 진공 상태에서의 빛의 속도를 의미합니다."
                        }
                    ]
                    },
                    "incorrect": {
                    "count": 3,
                    "questions": [
                        {
                        "subject": "수/과학",
                        "difficult": "하",
                        "question": "작은 생물도 관찰 가능한 광학 장비는?",
                        "select_1": "망원경",
                        "select_2": "현미경",
                        "select_3": "쌍안경",
                        "select_4": "굴절기",
                        "answer": 2,
                        "user_select": 4,
                        "explanation": "현미경은 작은 물체를 확대해 관찰하는 데 사용하는 장비입니다."
                        },
                        {
                        "subject": "예술",
                        "difficult": "중",
                        "question": "‘최후의 만찬’을 그린 화가는 누구인가요?",
                        "select_1": "레오나르도 다빈치",
                        "select_2": "미켈란젤로",
                        "select_3": "라파엘로",
                        "select_4": "카라바조",
                        "answer": 1,
                        "user_select": 4,
                        "explanation": "‘최후의 만찬’은 르네상스의 거장 레오나르도 다빈치의 대표작입니다."
                        },
                        {
                        "subject": "상식",
                        "difficult": "중상",
                        "question": "세계에서 가장 오래된 문명 중 하나인 메소포타미아는 현재 어느 지역에 있나요?",
                        "select_1": "이집트",
                        "select_2": "이라크",
                        "select_3": "터키",
                        "select_4": "이란",
                        "answer": 2,
                        "user_select": 1,
                        "explanation": "메소포타미아 문명은 현재 이라크 지역의 티그리스-유프라테스 강 사이에 존재했습니다."
                        }
                    ]
                    }
                
                }
            }
        }

class DailyQuizResponse(BaseModel):
    solved_index: int
    questions: List[QuestionInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "solved_index": 0,
                "questions": [
                    {
                        "subject": "수/과학",
                        "difficult": "하",
                        "question_id": 1,
                        "question": "대기 중 가장 많은 기체는?",
                        "select_1": "산소",
                        "select_2": "수소",
                        "select_3": "이산화탄소",
                        "select_4": "질소",
                        "answer": 4,
                        "explanation": "대기의 약 78%는 질소이며 가장 많은 기체입니다.",
                        "correct_rate": 69
                    },
                    {
                        "subject": "시사",
                        "difficult": "중",
                        "question_id": 2,
                        "question": "노벨 평화상을 수상한 최초의 여성은 누구인가요?",
                        "select_1": "마리 퀴리",
                        "select_2": "말랄라 유사프자이",
                        "select_3": "앙겔라 메르켈",
                        "select_4": "테레사 수녀",
                        "answer": 4,
                        "explanation": "테레사 수녀는 인도에서 봉사활동을 한 공로로 노벨 평화상을 받았습니다.",
                        "correct_rate": 92
                    }
                ]
            }
        }