from flask import Blueprint, request, jsonify
from app import db
from models import User
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/UsersFirst', methods=['POST'])
def UsersFirst():
    '''
    Post: Create the first user in the system
    needed when DB is empty
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            email = data['email']
            password = data['password']
            full_name = data['full_name']

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
            return jsonify({'message': 'Error creating first user', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405



@user_bp.route('/Users', methods=['POST','GET'])
@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    if request.method == 'POST':
        try:
            curr_user_id = get_jwt_identity()
            data = request.get_json()

            new_user = User(
                email=data['email'],
                full_name=data['full_name'],
                is_archived=data.get('is_archived', False),
                created_by=curr_user_id,
                updated_by=curr_user_id
             )

            new_user.set_password(data['password'])

            db.session.add(new_user)
            db.session.commit()

            return jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating user', 'error': str(e)}), 500


    elif request.method == 'GET':
        try:
            users = User.query.all()
            users_list = []

            for user in users:
                users_list.append({
                    'id': user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'created_at': user.created_at,
                    'updated_at': user.updated_at,
                    'is_archived': user.is_archived,
                    'created_by': user.created_by,
                    'updated_by': user.updated_by
                })

            return jsonify({'users': users_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting users', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed, only POST and GET are allowed'}), 405



@user_bp.route('/Users/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def User_id(id):
    '''
    GET: Get existing user from DB using user ID
    PUT: Update existing user in DB using user ID
    DELETE: archive existing user in DB using user ID
    '''
    if request.method == 'GET':
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            user = {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'is_archived': user.is_archived,
                'created_by': user.created_by,
                'updated_by': user.updated_by
            }

            return jsonify({'message': f'User with id:{id} retrieved successfully','user': user}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting user', 'error': str(e)}), 500
    

    elif request.method == 'PUT':
        try:
            
            data = request.get_json()
            user = User.query.get(id)

            if not user:
                return jsonify({'message': 'User not found'}), 404

            if 'email' in data:
                user.email = data['email']
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'password' in data:
                user.set_password(data['password'])
            if 'is_archived' in data:
                user.is_archived = data['is_archived']

            user.updated_by = get_jwt_identity() 

            db.session.commit()
            return jsonify({'message': 'User updated successfully'}), 200
        except Exception as e:
            return jsonify({'message': 'Error updating user', 'error': str(e)}), 500
        

    # No deletion of user, only archiving is allowed
    elif request.method == 'DELETE':
        try:
            user = User.query.get(id)

            if not user:
                return jsonify({'message': 'User not found'}), 404

            user.is_archived = True # only archive the user
            user.updated_by = get_jwt_identity() 

            db.session.commit()
            return jsonify({'message': 'User archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving user', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405
        
    
##### Check
@user_bp.route('/Users/<id>/Contracts', methods=['GET'])
@jwt_required()
def User_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific user
    '''
    if request.method == 'GET':
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404

            contracts = []
            for contract in user.contracts_created:
                contracts.append({
                    'id': contract.id,
                    'client_id': contract.client_id,
                    'contract_type': contract.contract_type,
                    'contract_name': contract.contract_name,
                    'created_at': contract.created_at,
                    'updated_at': contract.updated_at,
                    'is_archived': contract.is_archived
                })

            return jsonify({'contracts': contracts}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting user contracts', 'error': str(e)}), 500


    return jsonify({'message': 'Method not allowed'}), 405