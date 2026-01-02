from flask import Blueprint, request
from app import db
from models import User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error
from schemas.user_schema import user_read_schema

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    '''
    User Login using JWT authentication
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            if not data:
                return bad_request(message="Invalid request body")
            
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return bad_request(message="Email and password are required")
            
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return bad_request(message="Invalid credentials")
    
            # identity is user.id
            access_token = create_access_token(identity=user.id)
            
            return ok(data={"token": access_token}, message="Login successful")
           

        except Exception as e:
            return server_error(message="An error occurred during login")



@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    '''
    A test protected endpoint that requires a valid JWT to access
    '''
    try:
        current_user_id = get_jwt_identity() 
        current_user_id_obj = UUID(current_user_id) if isinstance(current_user_id, str) else current_user_id
        current_user = db.session.get(User, current_user_id_obj)
        
        if not current_user:
            return not_found(message="User not found")
        
        user_data = user_read_schema.dump(current_user)
        return ok(data=user_data, message="Protected endpoint accessed successfully")
        
    except Exception as e:
        return server_error(message="An error occurred while fetching user data", errors=str(e))

    
