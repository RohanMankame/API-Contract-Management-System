from flask import Blueprint, request, jsonify
from app import db
from models import Contract
from datetime import datetime
from flask_jwt_extended import jwt_required

# Initialize contract Blueprint
contract_bp = Blueprint('contract', __name__)

# Contract Endpoints

@contract_bp.route('/Contracts', methods=['POST','GET'])
@jwt_required()
def Contracts():
    '''
    Post: Create a new contract
    Get: Get all contracts from DB
    '''
    if request.method == 'POST':
        pass

    elif request.method == 'GET':
        pass

@contract_bp.route('/Contracts/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def Contract_id(id):
    '''
    GET: Get existing contract from DB using contract ID
    PUT: Update existing contract in DB using contract ID
    DELETE: Delete existing contract from DB using contract ID
    '''
    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        pass

    elif request.method == 'DELETE':
        pass


@contract_bp.route('/Contracts/<id>/Product', methods=['POST','GET'])
@jwt_required()
def Contract_Product_id(id):
    '''
    Post: new contract for a spefic product
    Get: get all contracts that use a specific product
    '''
    if request.method == 'POST':
        pass

        
    elif request.method == 'GET':
        pass
    


