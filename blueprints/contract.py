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
            client_id = data['client_id']
            contract_type = data['contract_type']
            contract_name = data['contract_name']
            is_archived = data.get('is_archived', False)

            user_email = get_jwt_identity()
            user = User.query.filter_by(email=user_email).first()
            user_id = user.id
            

            new_contract = Contract(
                client_id=client_id,
                contract_type=contract_type,
                created_by_user_id=user_id,
                updated_by_user_id=user_id,
                contract_name=contract_name,
                is_archived=is_archived
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
                    'contract_type': contract.contract_type,
                    'created_by_user_id': contract.created_by_user_id,
                    'updated_by_user_id': contract.updated_by_user_id,
                    'contract_name': contract.contract_name,
                    'created_at': contract.created_at,
                    'updated_at': contract.updated_at,
                    'is_archived': contract.is_archived
                })

            return jsonify({'contracts': contracts_list}), 200
    
        except Exception as e:
            return jsonify({'message': 'Error getting contracts', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405



@contract_bp.route('/Contracts/<id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required()
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
                'contract_type': contract.contract_type,
                'created_by_user_id': contract.created_by_user_id,
                'updated_by_user_id': contract.updated_by_user_id,
                'contract_name': contract.contract_name,
                'created_at': contract.created_at,
                'updated_at': contract.updated_at,
                'is_archived': contract.is_archived
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
            
            contract.client_id = data['client_id']
            contract.contract_type = data['contract_type']
            contract.updated_by_user_id = data['updated_by_user_id']
            contract.contract_name = data['contract_name']
            contract.is_archived = data.get('is_archived', contract.is_archived)
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
            db.session.commit()
            return jsonify({'message': 'Contract has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error deleting contract', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405


@contract_bp.route('/Contracts/<id>/Product', methods=['POST','GET'])
#@jwt_required()
def Contract_Product_id(id):
    '''
    Post: new contract for a spefic product
    Get: get all contracts that use a specific product
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()
            product_id = data['product_id']
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            new_subscription = Subscription(
                product_id=product_id,
                contract_id=contract.id,
                start_date=datetime.utcnow(),
                end_date=data.get('end_date')
            )

            db.session.add(new_subscription)
            db.session.commit()

            return jsonify({'message': 'Subscription created successfully', 'subscription_id': new_subscription.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating subscription for contract', 'error': str(e)}), 500

        
    elif request.method == 'GET':
        try:
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            subscriptions = contract.subscriptions
            products_list = []

            for subscription in subscriptions:
                product = subscription.product
                products_list.append({
                    'id': product.id,
                    'api_name': product.api_name,
                    'description': product.description,
                    'is_archived': product.is_archived,
                    'created_at': product.created_at,
                    'updated_at': product.updated_at
                })

            return jsonify({'products': products_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting products for contract', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405

