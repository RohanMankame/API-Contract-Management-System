from flask import Blueprint, request, jsonify
from app import db
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    '''
    User Login using JWT authentication
    '''
    if request.method == 'POST':
        try:
            if not request.is_json:
                return {"error": "Missing JSON in request"}, 400

            data = request.get_json()

            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()
            if not user or not user.check_password(password):
                return {"error": "Wrong Password or Username"}, 401

            access_token = create_access_token(identity=user.email)
            return {"access_token": access_token}, 200

        except Exception as e:
            return {"error": str(e)}, 500

    return {"error": "Invalid request method"}, 405


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    '''
    A test protected endpoint that requires a valid JWT to access
    '''
    current_user = get_jwt_identity() 
    if not current_user:
        return {"error": "User not found"}, 404

    return jsonify(logged_in_as=current_user), 200
