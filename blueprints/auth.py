from flask import Blueprint, request, jsonify
from app import db
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from uuid import UUID

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    '''
    User Login using JWT authentication
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            email = data['email']
            password = data['password']

            user = User.query.filter_by(email=email).first()
            if not user:
                return {"error": "User not found"}, 404

            if not user or not user.check_password(password):
                return {"error": "Wrong Password or Username"}, 401

            # identity is user.id
            access_token = create_access_token(identity=user.id)

            return {"access_token": access_token}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    return {"error": "Invalid request method"}, 405


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    '''
    A test protected endpoint that requires a valid JWT to access
    '''
    current_user_id = get_jwt_identity() 
    current_user_id_obj = UUID(current_user_id) if isinstance(current_user_id, str) else current_user_id
    current_user = db.session.get(User, current_user_id_obj)
    
    if not current_user:
        return {"error": "User not found"}, 404

    return jsonify(logged_in_as=current_user.email), 200
