from sqlalchemy import create_engine, Column, String, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'
    id = Column(String, primary_key=True)
    label = Column(String, nullable=False)
    type = Column(String(50), nullable=False)
    value = Column(String, nullable=False)
    image = Column(String)
    options = Column(PickleType)


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(String, primary_key=True)
    answer = Column(String(25000), nullable=False)
    question_id = Column(String, ForeignKey(
        'questions.id', ondelete='CASCADE'), nullable=False, unique=True)
    question = relationship("Question", backref="answers")


class Database:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri, echo=True)
        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)

    def create_question(self, **kwargs):
        with self.Session() as session:
            question = Question(**kwargs)
            session.add(question)
            session.commit()

    def get_unanswered_questions(self):
        with self.Session() as session:
            questions = session.query(Question).filter(
                Question.id.notin_(session.query(Answer.question_id)))
            return questions

    def delete_question(self, question_id):
        with self.Session() as session:
            question = session.query(Question).filter_by(
                id=question_id).first()
            if question:
                session.delete(question)
                session.commit()

    def create_answer(self, **kwargs):
        with self.Session() as session:
            answer = Answer(**kwargs)
            session.add(answer)
            session.commit()
            
    def delete_answer(self, answer_id):
        with self.Session() as session:
            answer = session.query(Answer).filter_by(
                id=answer_id).first()
            if answer:
                session.delete(answer)
                session.commit()

