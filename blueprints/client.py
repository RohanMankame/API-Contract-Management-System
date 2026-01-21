from flask import Blueprint, request
from app import db
from models import Client
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.client_schema import client_read_schema, clients_read_schema, client_write_schema
from schemas.contract_schema import contracts_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

# Initialize client Blueprint
client_bp = Blueprint('client', __name__)

# Client Endpoints
@client_bp.route('/clients', methods=['POST','GET'])
@jwt_required()
def Clients():    
    '''
    Post: Create a new client
    Get: Get all clients from DB
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = client_write_schema.load(data)

            new_client = Client(**validated, created_by=current_user_id, updated_by=current_user_id)

            db.session.add(new_client)
            db.session.commit()

            return created(data={"client": client_read_schema.dump(new_client)}, message="Client created successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error creating client", errors=str(e))






    elif request.method == 'GET':
        try:
            clients = db.session.query(Client).filter_by(is_archived=False).all()
            
            return ok(data={"clients": clients_read_schema.dump(clients)}, message="Clients retrieved successfully")

        except Exception as e:
            return server_error(message="Error retrieving clients", errors=str(e))


@client_bp.route('/clients/<id>', methods=['GET', 'PUT','PATCH', 'DELETE'])
@jwt_required()
def Client_id(id):
    '''
    GET: Get existing client from DB using client ID
    PUT: Update existing client in DB using client ID
    DELETE: Archive existing client from DB using client ID
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            client = db.session.query(Client).filter_by(id=id_obj, is_archived=False).first()

            
            if not client:
                return not_found(message="Client not found")
            
            return ok(data={"client": client_read_schema.dump(client)}, message="Client retrieved successfully")
        
        except Exception as e:
            #db.session.rollback()
            return server_error(message="Error retrieving client", errors=str(e))


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            partial = (request.method == 'PATCH')
            validated = client_write_schema.load(data, partial=partial)   

            id_obj = UUID(id) if isinstance(id, str) else id
            client = db.session.get(Client, id_obj)
            
            if not client:
                return not_found(message="Client not found")

            for key, value in validated.items():
                setattr(client, key, value)
            client.updated_by = current_user_id

            db.session.commit()

            return ok(data={"client": client_read_schema.dump(client)}, message="Client updated successfully")
        
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error updating client", errors=str(e))


    
    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            client = db.session.get(Client, id_obj)
            
            if not client:
                return not_found(message="Client not found")
            
            client.is_archived = True
            client.updated_by = current_user_id

            db.session.commit()
            return ok(data={"client": client_read_schema.dump(client)}, message="Client archived successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error archiving client", errors=str(e))


@client_bp.route('/clients/<id>/contracts', methods=['GET'])
@jwt_required()
def Client_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific client
    '''
    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            client = db.session.get(Client, id_obj)
            
            if not client:
                return not_found(message="Client not found")

            contracts = client.contracts
            return ok(data={"contracts": contracts_read_schema.dump(contracts)}, message="Contracts retrieved successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error retrieving contracts", errors=str(e))



