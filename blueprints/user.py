from flask import Blueprint, request, jsonify
from app import db
from models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/createUser', methods=['POST'])
def createUser():
    '''
    Create a new user and save in DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send user details in JSON format"}, 400
    
    data = request.get_json()
    try:
        user = User(
            username=data.get('username'),
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        db.session.add(user)
        db.session.commit()
        return {"message": "User created", "user_id": user.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
        

@user_bp.route('/getUsers', methods=['GET'])
def getUsers():
    '''
    Get all users from DB
    '''
    try:
        users = User.query.all()
        users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return {"users": users_list}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@user_bp.route('/getUser/<id>', methods=['GET'])
def getUserByID(id):
    '''
    Get existing user from DB using user ID
    '''
    try:
        user = User.query.get(id)
        if user:
            return {"id": user.id, "username": user.username, "email": user.email}, 200
        else:
            return {"error": "User not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 400
