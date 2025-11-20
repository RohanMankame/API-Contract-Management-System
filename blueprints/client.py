from flask import Blueprint, request, jsonify
from app import db
from models import Client
import validators
from flask_jwt_extended import jwt_required

# Initialize client Blueprint
client_bp = Blueprint('client', __name__)

# Client Endpoints

@client_bp.route('/Clients', methods=['POST','GET'])
#@jwt_required()
def Clients():
    '''
    Post: Create a new client
    Get: Get all clients from DB
    '''
    
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validate input
            if not data.get('username') or not data.get('email'):
                return jsonify({'message': 'Missing required fields'}), 400
            if not validators.email(data['email']):
                return jsonify({'message': 'Invalid email format'}), 400

            # Check for existing client
            if Client.query.filter_by(email=data['email']).first():
                return jsonify({'message': 'Client with given email already exists'}), 409

            # Create new client
            new_client = Client(
                username=data['username'],
                email=data['email']
            )

            db.session.add(new_client)
            db.session.commit()

            return jsonify({'message': 'Client created successfully', 'client_id': new_client.id}), 201
    
        except Exception as e:
            return jsonify({'message': 'Error creating client', 'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            clients = Client.query.all()
            clients_list = [{'id': client.id, 'username': client.username, 'email': client.email} for client in clients]
            return jsonify(clients_list), 200
        except Exception as e:
            return jsonify({'message': 'Error fetching clients', 'error': str(e)}), 500


@client_bp.route('/Clients/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def Client_id(id):
    '''
    GET: Get existing client from DB using client ID
    PUT: Update existing client in DB using client ID
    DELETE: Delete existing client from DB using client ID
    '''
    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass




@client_bp.route('/Clients/<id>/Contracts', methods=['GET'])
@jwt_required()
def Client_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific client
    '''
    if request.method == 'GET':
        pass

