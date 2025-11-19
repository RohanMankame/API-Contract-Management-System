from flask import Blueprint, request, jsonify
from app import db
from models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    '''
    User Login using JWT authentication
    '''
    if not request.is_json:
        return {"error": "Missing JSON in request"}, 400
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return {"error": "Wrong Password or Username"}, 401

    access_token = create_access_token(identity=user.username)
    return {"access_token": access_token}, 200



@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    '''
    A protected endpoint that requires a valid JWT to access
    '''
    current_user = get_jwt_identity() 
    if not current_user:
        return {"error": "User not found"}, 404

    return jsonify(logged_in_as=current_user), 200
