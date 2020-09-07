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
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

  def __repr__(self):
    return f'Todo: id:{self.id}, d:{self.description}, c:{self.completed}'

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)
  def __repr__(self):
    return f'TodoList: id:{self.id}, n:{self.name}'

@app.route('/')
def index():
  first_list = TodoList.query.order_by('id').first()
  return redirect(url_for('list_index', list_id=first_list.id))

@app.route('/lists/<list_id>')
def list_index(list_id):
  return render_template('index.html', 
    lists=TodoList.query.order_by('name').all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all(),
  )

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

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
  return jsonify({'success': True})

@app.route('/lists/<list_id>/todos', methods=['POST'])
def create_todo(list_id):
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description, list_id=list_id)
    body = {'description': todo.description }
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
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
