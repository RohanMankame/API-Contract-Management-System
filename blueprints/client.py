from flask import Blueprint, request, jsonify
from app import db
from models import Client
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.client_schema import client_read_schema, clients_read_schema, client_write_schema
from marshmallow import ValidationError

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
    curr_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = client_write_schema.load(data)

            new_client = Client(**validated,created_by=curr_user_id,updated_by=curr_user_id)

            db.session.add(new_client)
            db.session.commit()

            return jsonify(client=client_read_schema.dump(new_client)), 201
            
        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400

        

    elif request.method == 'GET':
        try:
            clients = Client.query.all()
            return jsonify(clients=clients_read_schema.dump(clients)), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400



@client_bp.route('/Clients/<id>', methods=['GET', 'PUT','PATCH', 'DELETE'])
@jwt_required()
def Client_id(id):
    '''
    GET: Get existing client from DB using client ID
    PUT: Update existing client in DB using client ID
    DELETE: Archive existing client from DB using client ID
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({"error": "Client not found"}), 404

            return jsonify(client=client_read_schema.dump(client)), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400



    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            validated = client_write_schema.load(data, partial=True)

            client = Client.query.get(id)
            if not client:
                return jsonify({"error": "Client not found"}), 404

            for key, value in validated.items():
                setattr(client, key, value)
            client.updated_by = curr_user_id

            db.session.commit()

            return jsonify(client=client_read_schema.dump(client)), 200

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400


    
    elif request.method == 'DELETE':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({"error": "Client not found"}), 404

            client.is_archived = True
            client.updated_by = curr_user_id

            db.session.commit()
            return jsonify({"message": "Client archived successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
"""
@client_bp.route('/Clients/<id>/Contracts', methods=['GET'])
@jwt_required()
def Client_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific client
    '''
    current_user_id = get_jwt_identity()
    if request.method == 'GET':
        try:
            client = Client.query.get(id)
            if not client:
                return jsonify({"error": "Client not found"}), 404

            contracts = client.contracts
            from schemas.contract_schema import contracts_read_schema
            return jsonify(contracts=contracts_read_schema.dump(contracts)), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400
"""
