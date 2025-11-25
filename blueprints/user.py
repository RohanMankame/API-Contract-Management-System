from flask import Blueprint, request, jsonify
from app import db
from models import User
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/Users', methods=['POST','GET'])
@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()
            curr_user = get_jwt_identity()
            
            curr_user_id = curr_user.id

            user_id = curr_user_id['id']

            email = data['email']
            password = data['password']
            full_name = data['full_name']

            new_user = User(email=email,
                full_name=full_name,
                created_by_id=curr_user_id,
                updated_by_id=curr_user_id
             )

            new_user.set_password(password)
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
                    'updated_at': user.updated_at
                })

            return jsonify({'users': users_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting users', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405


@user_bp.route('/Users/<id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required()
def User_id(id):
    '''
    GET: Get existing user from DB using user ID
    PUT: Update existing user in DB using user ID
    DELETE: Delete existing user from DB using user ID
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
                'updated_at': user.updated_at
            }

            return jsonify({'user': user}), 200
        except Exception as e:
            return jsonify({'message': 'Error getting user', 'error': str(e)}), 500
    

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            user = User.query.get(id)
            
            if not user:
                return jsonify({'message': 'User not found'}), 404
            
            user.email = data['email']
            user.full_name = data['full_name']
            
            if 'password' in data:
                user.set_password(data['password'])
            db.session.commit()

            return jsonify({'message': 'User updated successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': 'Error updating user', 'error': str(e)}), 500
        

    elif request.method == 'DELETE':
        try:
            user = User.query.get(id)
            if not user:
                return jsonify({'message': 'User not found'}), 404
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'User deleted successfully'}), 200
        except Exception as e:
            return jsonify({'message': 'Error deleting user', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405
        
    

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