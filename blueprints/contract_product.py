from flask import Blueprint, request, jsonify
from app import db
from models import ContractProduct
from flask_jwt_extended import jwt_required
# Initialize contract_product Blueprint
contract_product_bp = Blueprint('contract_product', __name__)

# ContractProduct Endpoints
@contract_product_bp.route('/ContractProducts', methods=['POST', 'GET'])
#@jwt_required()
def ContractProducts():
    '''
    Post: Create a new contract-product association
    Get: Get all contract-product associations from DB
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Validate input
            if not data.get('contract_id') or not data.get('product_id') or not data.get('subscription_type_id'):
                return jsonify({'message': 'Missing required fields'}), 400

            # Create new contract-product association
            new_ContractProduct = ContractProduct(
                contract_id=data['contract_id'],
                product_id=data['product_id'],
                subscription_type_id=data['subscription_type_id']
            )

            db.session.add(new_ContractProduct)
            db.session.commit()

            return jsonify({'message': 'Contract-Product association created successfully', 'id': new_cp.id}), 201


        except Exception as e:
            return jsonify({'message': 'Error creating contract-product association', 'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            contract_products = ContractProduct.query.all()
            cp_list = [{'id': cp.id, 'contract_id': cp.contract_id, 'product_id': cp.product_id, 'subscription_type_id': cp.subscription_type_id} for cp in contract_products]
            return jsonify(cp_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching contract-product associations', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 500

@contract_product_bp.route('/ContractProducts/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def ContractProduct_id(id):
    '''
    Get: Get details of specific contract-product association
    Put: Update details of contract-product association with given ID
    Delete: Delete contract-product association with given ID
    '''
    if request.method == 'GET':
        try:
            pass

        except Exception as e:
            return jsonify({'message': 'Error fetching contract-product association', 'error': str(e)}), 500

    elif request.method == 'PUT':
        try:
            pass

        except Exception as e:
            return jsonify({'message': 'Error updating contract-product association', 'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            pass
        
        except Exception as e:
            return jsonify({'message': 'Error deleting contract-product association', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 500

    @contract_bp.route('/ContractProducts/<id>/Details', methods=['GET'])
    @jwt_required()
    def ContractProduct_Details_id(id):
        '''
        Get: Get details of specific contract-product association
        '''