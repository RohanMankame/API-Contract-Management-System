from flask import Blueprint, request, jsonify
from app import db
from models import Contract, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        try:
            data = request.get_json()

            new_contract = Contract(
                client_id=data['client_id'],
                contract_name=data['contract_name'],
                is_archived=data.get('is_archived', False),
                
                created_by = get_jwt_identity(),
                updated_by = get_jwt_identity()
            )

            db.session.add(new_contract)
            db.session.commit()

            return jsonify({'message': 'Contract created successfully', 'contract_id': new_contract.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating contract', 'error': str(e)}), 500
    

    elif request.method == 'GET':
        try:
            contracts = Contract.query.all()
            contracts_list = []

            for contract in contracts:
                contracts_list.append({
                    'id': contract.id,
                    'client_id': contract.client_id,
                    'contract_name': contract.contract_name,
                    
                    'is_archived': contract.is_archived,                
                    'created_at': contract.created_at,
                    'updated_at': contract.updated_at,
                    'created_by': contract.created_by,
                    'updated_by': contract.updated_by
                })

            return jsonify({'contracts': contracts_list}), 200
    
        except Exception as e:
            return jsonify({'message': 'Error getting contracts', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405



@contract_bp.route('/Contracts/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def Contract_id(id):
    '''
    GET: Get existing contract from DB using contract ID
    PUT: Update existing contract in DB using contract ID
    DELETE: Delete existing contract from DB using contract ID
    '''
    if request.method == 'GET':
        try:
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            contract_data = {
                    'id': contract.id,
                    'client_id': contract.client_id,
                    'contract_name': contract.contract_name,
                   
                    'is_archived': contract.is_archived,                
                    'created_at': contract.created_at,
                    'updated_at': contract.updated_at,
                    'created_by': contract.created_by,
                    'updated_by': contract.updated_by
            }

            return jsonify({'contract': contract_data}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting contract', 'error': str(e)}), 500
    

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404
            
            if 'client_id' in data:
                contract.client_id = data['client_id']
            if 'contract_name' in data:
                contract.contract_name = data['contract_name']
            if 'is_archived' in data:
                contract.is_archived = data['is_archived']
            
            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Contract updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating contract', 'error': str(e)}), 500


    elif request.method == 'DELETE':
        try:
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            contract.is_archived = True
            
            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Contract has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error deleting contract', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405


@contract_bp.route('/Contracts/<id>/Product', methods=['POST','GET'])
@jwt_required()
def Contract_Product_id(id):
    '''
    Get: Get all products associated with a specific contract ID
    '''
    try:
        contract = Contract.query.get(id)
        if not contract:
            return jsonify({'message': 'Contract not found'}), 404

        products_list = []
        
        
        for subscription in contract.subscriptions:
            product = subscription.product 
            
            
            if not any(p['id'] == str(product.id) for p in products_list):
                products_list.append({
                    'id': str(product.id),
                    'api_name': product.api_name,  
                    'description': product.description,
                    'is_archived': product.is_archived,
                    'created_at': product.created_at.isoformat() if product.created_at else None,
                    'updated_at': product.updated_at.isoformat() if product.updated_at else None,
                    'created_by': str(product.created_by) if product.created_by else None,
                    'updated_by': str(product.updated_by) if product.updated_by else None
                })

        return jsonify({'products': products_list}), 200
    
    
    except Exception as e:
        return jsonify({'message': 'Error getting products', 'error': str(e)}), 500