from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
  age = db.Column(db.Integer, db.CheckConstraint('age>0'))

  def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}, age: >'

# create all new tables
db.create_all()


@app.route('/')
def index():
  return "hello {}".format(Person.query.first().name)


if __name__ == '__main__':
  app.run()
