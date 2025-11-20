from flask import Blueprint, request, jsonify, make_response
from app import db
from models import User
import validators
from flask_jwt_extended import jwt_required

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/Users', methods=['POST','GET'])
#@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validate input
            if not data.get('username') or not data.get('email') or not data.get('password'):
                return make_response(jsonify({'message': 'Missing required fields'}), 400)
            if not validators.email(data['email']):
                return make_response(jsonify({'message': 'Invalid email format'}), 400)

            # Check for existing user
            if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
                return make_response(jsonify({'message': 'User with given username or email already exists'}), 409)

            # Create new user
            new_user = User(
                username=data['username'],
                email=data['email']
            )
            new_user.set_password(data['password'])

            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify({'message': 'User created successfully', 'user_id': new_user.id}), 201)

        except Exception as e:
            return make_response(jsonify({'message': 'Error creating user', 'error': str(e)}), 500)



    elif request.method == 'GET':
        try:
            users = User.query.all()
            users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return make_response(jsonify(users_list), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Error fetching users', 'error': str(e)}), 500)




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
                return make_response(jsonify({'message': 'User not found'}), 404)

            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            return make_response(jsonify(user_data), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Error fetching user', 'error': str(e)}), 500)


    elif request.method == 'PUT':
        try:
            data = request.get_json()
            user = User.query.get(id)
            if not user:
                return make_response(jsonify({'message': 'User not found'}), 404)

            # Update fields if provided
            if data.get('username'):
                user.username = data['username']
            if data.get('email'):
                if not validators.email(data['email']):
                    return make_response(jsonify({'message': 'Invalid email format'}), 400)
                user.email = data['email']
            if data.get('password'):
                user.set_password(data['password'])

            db.session.commit()
            return make_response(jsonify({'message': 'User updated successfully'}), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Error updating user', 'error': str(e)}), 500)
    

    elif request.method == 'DELETE':
        try:
            user = User.query.get(id)
            if not user:
                return make_response(jsonify({'message': 'User not found'}), 404)

            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'User deleted successfully'}), 200)

        except Exception as e:
            return make_response(jsonify({'message': 'Error deleting user', 'error': str(e)}), 500)
    



@user_bp.route('/Users/<id>/Contracts', methods=['GET'])
@jwt_required()
def User_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific user
    '''
    try:
        user = User.query.get(id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)

        contracts = []  # Assuming a relationship exists to fetch contracts
        for contract in user.contracts:
            contracts.append({
                'contract_id': contract.contract_id,
                'client_id': contract.client_id,
                'product_id': contract.product_id,
                'start_date': contract.start_date,
                'end_date': contract.end_date
            })

        return make_response(jsonify(contracts), 200)

    except Exception as e:
        return make_response(jsonify({'message': 'Error fetching contracts', 'error': str(e)}), 500)