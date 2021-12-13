import sys

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

template_dir = '../client' #relative path from ./src/server
app = Flask(__name__)
uri_string = 'postgresql://localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todo_id = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList (self.id), {self.name}>'

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}, {self.description}>'


# db.create_all()

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    todos = Todo.query.filter_by(list_id=list_id).order_by('id').all()
    lists = TodoList.query.all()
    active_list = TodoList.query.get(list_id)
    return render_template('index.html', lists=lists, todos=todos,
                            active_list=active_list)

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/todos/create', methods=['POST'])
def create():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        print(description)
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body['description'] = todo.description
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


@app.route('/todos/<todo_id>/set-completed', methods=["POST"])
def set_complete_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>/delete', methods=["DELETE"])
def delete_todo(todo_id):
    result = {'success': True}
    print("in delete_todo")
    print('id', todo_id)
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        result = {'success': False}
        db.session.rollback
    finally:
        db.session.close()
    # return redirect(url_for('index'))
    return jsonify(result)
