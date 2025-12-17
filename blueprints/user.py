from flask import Blueprint, request
from app import db
from models import User, Contract
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user_schema import user_read_schema, users_read_schema, user_write_schema
from schemas.contract_schema import contracts_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/users-first', methods=['POST'])
def UsersFirst():
    '''
    Post: Create the first user in the system
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            email = data['email']
            password = data['password']
            full_name = data['full_name']

            if not all([email, password, full_name]):
                return bad_request(message="Missing required fields: email, password, full_name")

            new_user = User(
                email=email,
                full_name=full_name,
                created_by=None,
                updated_by=None
             )

            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return created(data={"user_id": str(new_user.id)}, message="First user created successfully")
        
        except Exception as e:
            db.session.rollback()
            return bad_request(message="Error creating first user", errors=str(e))


@user_bp.route('/users', methods=['POST','GET'])
@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = user_write_schema.load(data)

            password = validated.pop('password', None)
            new_user = User(**validated, created_by=current_user_id, updated_by=current_user_id)
            if password:
                new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return created(data={"user": user_read_schema.dump(new_user)}, message="User created successfully")


        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation error", errors=str(ve.messages))

        except Exception as e:
            db.session.rollback()
            return bad_request(message="Error creating user", errors=str(e))
    
    
    elif request.method == 'GET':
        try:
            users = User.query.all()
            return ok(data={"users": users_read_schema.dump(users)}, message="Users retrieved successfully")
        
        except Exception as e:
            return bad_request(message="Error retrieving users", errors=str(e))


@user_bp.route('/users/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required()
def User_id(id):
    '''
    GET: Get existing user from DB using user ID
    PUT: Update existing user in DB using user ID
    DELETE: archive existing user in DB using user ID
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return not_found(message="User not found")

            return ok(data={"user": user_read_schema.dump(user)}, message="User retrieved successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error getting user")



    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            

            if not user:
                return not_found(message="User not found")

            validated = user_write_schema.load(data, partial=True)

            for key, value in validated.items():
                if key == 'password':
                    user.set_password(value)
                else:
                    setattr(user, key, value)

            user.updated_by = current_user_id

            db.session.commit()
            return ok(data={"user": user_read_schema.dump(user)}, message="User updated successfully")
        

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation error", errors=ve.messages)
        
        except Exception as e:
            db.session.rollback()
            return server_error(message="Error updating user", errors=str(e))
    
    
    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return not_found(message="User not found")

            user.is_archived = True 
            user.updated_by = current_user_id

            db.session.commit()
            return ok(data={"user": user_read_schema.dump(user)}, message="User archived successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error archiving user", errors=str(e))


@user_bp.route('/users/<id>/contracts', methods=['GET'])
@jwt_required()
def User_Contracts_id(id):
    '''
    Get: Get all contracts created by a user
    '''
    #current_user_id = get_jwt_identity()
    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return not_found(message="User not found")

            contracts_objs = db.session.query(Contract).filter(Contract.created_by==id_obj).all()
           
            contracts = contracts_read_schema.dump(contracts_objs)

            return ok(data={"contracts": contracts}, message="Contracts retrieved successfully")
        
        except Exception as e:
            return server_error(message="Error getting contracts", errors=str(e))



