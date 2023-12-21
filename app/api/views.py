from flask import jsonify, request
from flask_login import login_user, current_user
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from config import config

from . import api_bp

from app.todo.models import Todo
from app.users.models import User

from app import db
from app import basic_auth


@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        "message": "pong"
    })


@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    
    todo_dict = []
    
    for todo in todos:
        item = dict(
            id = todo.id,
            title = todo.title,
            description = todo.description,
            complete = todo.complete
        )
        
        todo_dict.append(item)
        
    return jsonify(todo_dict)


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def post_todos():
    new_data = request.get_json()
    
    if not new_data:
        return jsonify({"message": "no input data provided"}), 400
    
    if not new_data.get('title'):
        return jsonify({"message": "not keys"}), 422 
    
    todo = Todo(title=new_data.get('title'))
    
    db.session.add(todo)
    db.session.commit()
    
    new_todo = Todo.query.filter_by(id=todo.id).first()
    
    return jsonify({
        #"message": "todo was add"
        "id": new_todo.id,
        "title": new_todo.title
    }), 201
    

@api_bp.route('/todos/<int:id>', methods=['GET'])
@jwt_required()
def get_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    if not todo:
        return jsonify({"message": f"todo with id = {id} not found"}), 404
    
    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description
    }), 200
    

@api_bp.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    todo = Todo.query.filter_by(id=id).first()
    
    if not todo:
        return jsonify({"message": f"todo with id = {id} not found"}), 404
    
    new_data = request.get_json()
    
    if not new_data:
        return jsonify({"message": "no input data provided"}), 400
    
    if new_data.get('title'):
        todo.title = new_data.get('title')
    
    if new_data.get('description'):
        todo.description = new_data.get('description')
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()

        
    return jsonify({
        "message": "todo was updated"
    }), 204
    

@api_bp.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
      todo = Todo.query.get(id)
      db.session.delete(todo)
      db.session.commit()
      return jsonify({"message" : "Resource successfully deleted."}), 200



#lab 14

@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        return username
    

@basic_auth.error_handler
def user_error(status):
    return jsonify(message = "Wrong") , status


@api_bp.route('/login', methods=['POST'])
@basic_auth.login_required
def login():
    auth = request.authorization

    user = User.query.filter_by(username=auth.username).first()
    if not user or not user.verify_password(auth.password):
        return jsonify({"message": "Invalid credentials"}), 401

    login_user(user)

    access_token = generate_access_token(user.username)
    
    return jsonify({"access_token": access_token}), 200


def generate_access_token(username):
    access_token = create_access_token(identity=username, expires_delta=timedelta(minutes=30))
    return access_token