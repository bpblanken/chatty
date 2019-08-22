from sqlalchemy import (
    create_engine,
    CheckConstraint, 
    Column,
    DateTime, 
    Enum, 
    ForeignKey, 
    Integer, 
    String
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from datetime import datetime
import enum

Base = declarative_base()

class TimestampMixin:
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class Gender(enum.Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    NON_BINARY = 'NON_BINARY'
 
class Topic(TimestampMixin, Base):
    __tablename__ = 'topics'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    questions = relationship("Question", backref="topic")
    
    def __init__(self, title):
        self.title = title

class Question(TimestampMixin, Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_texts = relationship("QuestionText", backref="question", \
        order_by="QuestionText.created_on")
    send_events = relationship("SendEvent", backref="question", lazy=True)
    receive_events = relationship("ReceiveEvent", backref="question", lazy=True)

    def __repr__(self):
        s = f"Question Id #{self.id}: \n"
        question_texts = [f"\t  Question Text: {x.text}" for x in self.question_texts]
        if len(question_texts) >= 2:
            question_texts[0] = question_texts[0].replace("\t  ", "(Initial) ")
            question_texts[-1] = question_texts[-1].replace("\t  ", "(Current) ")
        elif len(question_texts) == 0:
            question_texts = ["EMPTY"]
        s += "\n".join(question_texts)
        return s
    
class QuestionText(TimestampMixin, Base):
    __tablename__ = 'question_texts'
    id = Column(Integer, primary_key=True)
    text = Column(String(200), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    def __init__(self, text):
        self.text = text

class User(TimestampMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    gender = Column(Enum(Gender), nullable=False) 
    age = Column(Integer, nullable=False)
    send_events = relationship("SendEvent", backref="user")
    receive_events = relationship("ReceiveEvent", backref="user")
    
    __table_args__ = (
        CheckConstraint('age >= 18', name='age'),
    )

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

class SendEvent(TimestampMixin, Base):
    __tablename__ = 'send_events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

class ReceiveEvent(TimestampMixin, Base):
    __tablename__ = 'receive_events'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    text = Column(String(200), nullable=False)
    
    def __init__(self, text):
        self.text = text

def create_schema(conn_string):
    db = create_engine(conn_string)
    if not database_exists(db.url):
        create_database(db.url)
    Base.metadata.create_all(db)

def get_session(conn_string):
    db = create_engine(conn_string)
    Session = sessionmaker(bind=db)
    return Session()

