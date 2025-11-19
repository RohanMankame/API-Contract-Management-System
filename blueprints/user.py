from flask import Blueprint, request, jsonify, make_response
from app import db
from models import User
import validators

# Initialize Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/createUser', methods=['POST'])
def createUser():
    '''
    Create a new user and save in DB (Represents employees of the business)
    '''
    if not request.is_json:
        return {"error": "Invalid input, send details in JSON format"}, 400
    
    data = request.get_json()
    
    # Validate email format and username/password length
    if not validators.email(data.get('email')) or len(data.get('username')) < 5 or len(data.get('password')) < 5:
        return {"error": "Invalid email format or Username/Password is too short"}, 400

    try:
        user = User(
            username=data.get('username'),
            email=data.get('email')
            )
        user.set_password(data.get('password')) # set_password hashes the password
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
        users_list = [{"id": user.id, "username": user.username, "email": user.email, "hashed_password":user.password_hash} for user in users]
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
            return {"id": user.id, "username": user.username, "email": user.email, "hashed_password":user.password_hash}, 200
        else:
            return {"error": "User not found"}, 404
            
    except Exception as e:
        return {"error": str(e)}, 400
