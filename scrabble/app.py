from flask import Flask, render_template, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///scrabble'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Letters(db.Model):
  __tablename__ = 'letters'
  id = db.Column(db.Integer, primary_key=True)
  letters = db.Column(db.String, nullable=False)

  def __repr__(self):
    return f'Letters: id:{self.id}, data:{self.letters}'

class Word(db.Model):
  __tablename__ = 'words'
  id = db.Column(db.Integer, primary_key=True)
  word = db.Column(db.String, nullable=False)

  def __repr__(self):
    return f'Word: id:{self.id}, data:{self.word}'


db.create_all()


@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())

@app.route('/words', methods=['POST'])
# https://wordfinder.yourdictionary.com/unscramble/erteart
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    body = {'description': todo.description }
    db.session.add(todo)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(500)
  else:
    return jsonify(body)
    

if __name__ == '__main__':
  app.run()
