from sqlalchemy import (
    create_engine
    CheckConstraint, 
    Column,
    DateTime, 
    Enum, 
    ForeignKey, 
    Integer, 
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
import enum

Base = declarative_base()

class TimestampMixin:
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Gender(enum.Enum):
    male = 'MALE'
    female = 'FEMALE'
    nonbinary = 'NON_BINARY'
 
class Topic(TimestampMixin, Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    questions = relationship("Question", back_ref="topic")

class Question(TimestampMixin, Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_texts = relationship("QuestionText", back_ref="question")
    send_events = relationship("SendEvent", back_ref="question", True)
    receive_events = relationship("ReceiveEvent", back_ref="question", lazy=True)

class QuestionText(TimestampMixin, Base):
    __tablename__ = 'question_texts'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

class User(TimestampMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    gender = Column(Enum(Gender), nullable=False) 
    age = Column(Integer, nullable=False)
    send_events = relationship("SendEvent", back_ref="user")
    receive_events = relationship("ReceiveEvent", back_ref="user")
    
    __table_args__ = (
        CheckConstraint('age >= 18', name='age')
    )

class SendEvent(TimestampMixin, Base):
    __tablename__ = 'send_events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

class ReceiveEvent(TimestampMixin, Base)
    __tablename__ = 'receive_events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(String(200), nullable=False)

def create_schema(conn_string):
    db = create_engine(conn_string)
    Base.metadata.create_all(db)

