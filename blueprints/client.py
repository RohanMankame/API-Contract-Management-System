from flask import Blueprint, request, jsonify
from app import db
from models import Client
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity

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
    # need to still add validation for email and phone number
    if request.method == 'POST':
        try:
            data = request.get_json()

            company_name = data['company_name']
            email = data['email']
            phone_number = data['phone_number']
            address = data['address']
            is_archived = data['is_archived'] if 'is_archived' in data else False

            

            new_client = Client(
                company_name = company_name,
                email = email,
                phone_number = phone_number,
                address = address,
                is_archived = is_archived
                
                
            )
            db.session.add(new_client)
            db.session.commit()

            return jsonify({'message': 'Client created successfully'}), 201

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
                    'created_at': client.created_at,
                    'updated_at': client.updated_at
                })

            return jsonify({'clients': clients_list}), 200
        
        except Exception as e:
            return jsonify({'message': 'Error getting clients', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405



@client_bp.route('/Clients/<id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required()
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
                'created_at': client.created_at,
                'updated_at': client.updated_at
            }

            return jsonify({'message': f'Client with id:{id} retrieved successfully','client': client}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting client', 'error': str(e)}), 500


    elif request.method == 'PUT':
        try:
            data = request.get_json()
            client = Client.query.get(id)

            if not client:
                return jsonify({'message': 'Client not found'}), 404

            client.company_name = data['company_name']
            client.email = data['email']
            client.phone_number = data['phone_number']
            client.address = data['address']
            db.session.commit()

            client = Client.query.get(id)

            return jsonify({'message': f'Client with id:{id} updated successfully'}), 200


        except Exception as e:
            return jsonify({'message': 'Error updating client', 'error': str(e)}), 500

    '''
    elif request.method == 'DELETE':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({'message': 'Client not found'}), 404
            db.session.delete(client)
            db.session.commit()
            return jsonify({'message': 'Client deleted successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error deleting client', 'error': str(e)}), 500
    '''

    return jsonify({'message': 'Method not allowed'}), 405


@client_bp.route('/Clients/<id>/Contracts', methods=['GET'])
#@jwt_required()
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
                    'id': contract.id,
                    'contract_name': contract.contract_name,
                    'start_date': contract.start_date,
                    'end_date': contract.end_date,
                    'status': contract.status,
                    'created_at': contract.created_at,
                    'updated_at': contract.updated_at
                })

            return jsonify({'contracts': contracts_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting contracts for client', 'error': str(e)}), 500

