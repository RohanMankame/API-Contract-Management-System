from flask import Blueprint, request, jsonify
from app import db
from models import User, Contract
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.user_schema import user_read_schema, users_read_schema, user_write_schema
from schemas.contract_schema import contracts_read_schema
from marshmallow import ValidationError
from uuid import UUID

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints


@user_bp.route('/UsersFirst', methods=['POST'])
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
                return jsonify({'message': 'Missing required fields: email, password, full_name'}), 400

            new_user = User(
                email=email,
                full_name=full_name,
                created_by=None,
                updated_by=None
             )

            new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'First user created successfully', 'user_id': new_user.id}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error creating first user', 'error': str(e)}), 400



@user_bp.route('/Users', methods=['POST','GET'])
@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = user_write_schema.load(data)

            password = validated.pop('password', None)
            new_user = User(**validated, created_by=curr_user_id, updated_by=curr_user_id)
            if password:
                new_user.set_password(password)

            db.session.add(new_user)
            db.session.commit()

            return jsonify({"message": "User created successfully", "user": user_read_schema.dump(new_user)}), 201
            
        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400
    
    
    elif request.method == 'GET':
        try:
            users = User.query.all()
            return jsonify({"message": "Users retrieved successfully", "users": users_read_schema.dump(users)}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400




@user_bp.route('/Users/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
@jwt_required()
def User_id(id):
    '''
    GET: Get existing user from DB using user ID
    PUT: Update existing user in DB using user ID
    DELETE: archive existing user in DB using user ID
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404

            return jsonify({"message": "User retrieved successfully", "user": user_read_schema.dump(user)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error getting user', 'error': str(e)}), 500



    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            

            if not user:
                return jsonify({'error': 'User not found'}), 404

            validated = user_write_schema.load(data, partial=True)

            for key, value in validated.items():
                if key == 'password':
                    user.set_password(value)
                else:
                    setattr(user, key, value)

            user.updated_by = curr_user_id

            db.session.commit()
            return jsonify({'message': 'User updated successfully', "user": user_read_schema.dump(user)}), 200

        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error updating user', 'error': str(e)}), 500
    
    
    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return jsonify({'error': 'User not found'}), 404

            user.is_archived = True 
            user.updated_by = curr_user_id

            db.session.commit()
            return jsonify({'message': 'User archived successfully', "user": user_read_schema.dump(user)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error archiving user', 'error': str(e)}), 500



@user_bp.route('/Users/<id>/Contracts', methods=['GET'])
@jwt_required()
def User_Contracts_id(id):
    '''
    Get: Get all contracts created by a user
    '''
    curr_user_id = get_jwt_identity()
    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            user = db.session.get(User, id_obj)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404

            contracts_objs = db.session.query(Contract).filter(Contract.created_by==id_obj).all()
            #contracts_objs = Contract.query.filter_by(created_by=id).all()
            contracts = contracts_read_schema.dump(contracts_objs)

            return jsonify({'contracts': contracts}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': 'Error getting contracts', 'error': str(e)}), 500



