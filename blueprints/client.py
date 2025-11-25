from flask import Blueprint, request, jsonify
from app import db
from models import Client
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity

# Initialize client Blueprint
client_bp = Blueprint('client', __name__)

# Client Endpoints

@client_bp.route('/Clients', methods=['POST','GET'])
@jwt_required()
def Clients():
    '''
    Post: Create a new client
    Get: Get all clients from DB
    '''
    if request.method == 'POST':
        try:
            curr_user_id = get_jwt_identity()
            data = request.get_json()

            new_client = Client(
                company_name = data['company_name'],
                email = data['email'],
                phone_number = data['phone_number'],
                address = data['address'],
                is_archived = data.get('is_archived', False),
                created_by = curr_user_id,
                updated_by = curr_user_id
            )

            db.session.add(new_client)
            db.session.commit()

            return jsonify({'message': 'Client created successfully', 'client_id': new_client.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating client', 'error': str(e)}), 500


    elif request.method == 'GET':
        try:
            clients = Client.query.all()
            clients_list = []

            for client in clients:
                clients_list.append({
                    'id': client.id,
                    'company_name': client.company_name,
                    'email': client.email,
                    'phone_number': client.phone_number,
                    'address': client.address,
                    'is_archived': client.is_archived,
                    'created_at': client.created_at,
                    'updated_at': client.updated_at,
                    'created_by': client.created_by,
                    'updated_by': client.updated_by
                })

            return jsonify({'clients': clients_list}), 200
        
        except Exception as e:
            return jsonify({'message': 'Error getting clients', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed, only POST and GET are allowed'}), 405



@client_bp.route('/Clients/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def Client_id(id):
    '''
    GET: Get existing client from DB using client ID
    PUT: Update existing client in DB using client ID
    DELETE: Delete existing client from DB using client ID
    '''
    if request.method == 'GET':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({'message': 'Client not found'}), 404

            client = {
                'id': client.id,
                'company_name': client.company_name,
                'email': client.email,
                'phone_number': client.phone_number,
                'address': client.address,
                'is_archived': client.is_archived,
                'created_at': client.created_at,
                'updated_at': client.updated_at,
                'created_by': client.created_by,
                'updated_by': client.updated_by
            }

            return jsonify({'message': f'Client with id:{id} retrieved successfully','client': client}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting client', 'error': str(e)}), 500


    elif request.method == 'PUT':
        try:
            curr_user_id = get_jwt_identity()
            data = request.get_json()
            client = Client.query.get(id)

            if not client:
                return jsonify({'message': 'Client not found'}), 404

            if 'company_name' in data:
                client.company_name = data['company_name']
            if 'email' in data:
                client.email = data['email']
            if 'phone_number' in data:
                client.phone_number = data['phone_number']
            if 'address' in data:
                client.address = data['address']
            if 'is_archived' in data:
                client.is_archived = data['is_archived']
            client.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': f'Client with id:{id} updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating client', 'error': str(e)}), 500

    
    elif request.method == 'DELETE':
        try:
            curr_user_id = get_jwt_identity()
            client = Client.query.get(id)

            if not client:
                return jsonify({'message': 'Client not found'}), 404

            client.is_archived = True
            client.updated_by = curr_user_id
            
            db.session.commit()
            return jsonify({'message': 'Client deleted successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error deleting client', 'error': str(e)}), 500
    

    return jsonify({'message': 'Method not allowed'}), 405


@client_bp.route('/Clients/<id>/Contracts', methods=['GET'])
@jwt_required()
def Client_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific client
    '''
    if request.method == 'GET':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({'message': 'Client not found'}), 404

            contracts = client.contracts
            contracts_list = []

            for contract in contracts:
                contracts_list.append({
                    'id': client.id,
                    'company_name': client.company_name,
                    'email': client.email,
                    'phone_number': client.phone_number,
                    'address': client.address,
                    'is_archived': client.is_archived,
                    'created_at': client.created_at,
                    'updated_at': client.updated_at,
                    'created_by': client.created_by,
                    'updated_by': client.updated_by
                })

            return jsonify({'contracts': contracts_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting contracts for client', 'error': str(e)}), 500

