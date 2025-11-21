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
        pass
        
    elif request.method == 'GET':
        pass

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

