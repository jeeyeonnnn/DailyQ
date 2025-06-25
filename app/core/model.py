from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = "region"

    id = Column(BigInteger, primary_key=True, index=True)
    main_id = Column(Integer, nullable=False)
    main = Column(String(10), nullable=False)
    sub = Column(String(10), nullable=False)


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    region_id = Column(BigInteger, ForeignKey("region.id"), nullable=False)
    name = Column(String, index=True)
    user_id = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    pet_type = Column(Integer, nullable=False)
    level = Column(Integer, nullable=False, default=1)
    created_at = Column(DATETIME, nullable=False)


class Subject(Base):
    __tablename__ = "subject"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Difficult(Base):
    __tablename__ = "difficult"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Question(Base):
    __tablename__ = "question"

    id = Column(BigInteger, primary_key=True, index=True)
    subject_id = Column(BigInteger, ForeignKey("subject.id"), nullable=False)
    difficult_id = Column(BigInteger, ForeignKey("difficult.id"), nullable=False)
    name = Column(String, nullable=False)
    select_1 = Column(String, nullable=False)
    select_2 = Column(String, nullable=False)
    select_3 = Column(String, nullable=False)
    select_4 = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    explanation = Column(String, nullable=False)


class Exam(Base):
    __tablename__ = "exam"

    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False, primary_key=True)
    question_id = Column(BigInteger, ForeignKey("question.id"), nullable=False, primary_key=True)
    is_correct = Column(Integer, nullable=False)
    choose= Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    created_date = Column(DATETIME, nullable=False)


class Profile(Base):
    __tablename__ = "profile"

    pet_type = Column(BigInteger, primary_key=True, index=True)
    level = Column(BigInteger, primary_key=True, index=True)
    mypage = Column(String, nullable=False)
    ranking = Column(String, nullable=False)
    chat = Column(String, nullable=False)


class ChatRoom(Base):
    __tablename__ = "chat_room"

    id = Column(BigInteger, primary_key=True, index=True)
    user_1_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    user_2_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    created_at = Column(DATETIME, nullable=False)

class Chat(Base):
    __tablename__ = "chat"

    id = Column(BigInteger, primary_key=True, index=True)
    room_id = Column(BigInteger, ForeignKey("chat_room.id"), nullable=False)
    sender_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    content = Column(String, nullable=False)
    is_read = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False)
    
    
class Report(Base):
    __tablename__ = "report"

    id = Column(BigInteger, primary_key=True, index=True)
    date = Column(DATETIME, nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    is_title = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    order = Column(Integer, nullable=False)