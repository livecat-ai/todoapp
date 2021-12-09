import sys

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

template_dir = '../client' #relative path from ./src/server
app = Flask(__name__, template_folder=template_dir)
uri_string = 'postgresql://localhost:5432/todoapp'
app.config['SQLALCHEMY_DATABASE_URI'] = uri_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id}, {self.desctription}>'

db.create_all()

@app.route('/')
def index():
    results = Todo.query.all()
    return render_template('index.html', data = results)

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
