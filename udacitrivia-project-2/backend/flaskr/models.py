from sqlalchemy import Column, String, Integer
from flaskr import db


class Question(db.Model):
    """
    Trivia Question
    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty, id=None):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
        }


class Category(db.Model):
    """
    Trivia Category
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)

    def __init__(self, type, id=None):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
