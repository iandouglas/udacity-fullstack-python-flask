from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=False)

  def __repr__(self):
    return f'Todo: id:{self.id}, d:{self.description}, c:{self.completed}'



@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('id').all())

@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def change_todo(todo_id):
  try:
    todo = Todo.query.get(todo_id)
    todo.completed = request.get_json()['completed']
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('index'))

@app.route('/todos', methods=['POST'])
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
