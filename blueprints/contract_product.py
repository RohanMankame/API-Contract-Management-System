from flask import Blueprint, request, jsonify
from app import db
from models import ContractProduct
from flask_jwt_extended import jwt_required
# Initialize contract_product Blueprint
contract_product_bp = Blueprint('contract_product', __name__)

# ContractProduct Endpoints
@contract_product_bp.route('/ContractProducts', methods=['POST', 'GET'])
@jwt_required()
def ContractProducts():
    '''
    Post: Create a new contract-product association
    Get: Get all contract-product associations from DB
    '''
    if request.method == 'POST':
        try:
            pass


        except Exception as e:
            return jsonify({'message': 'Error creating contract-product association', 'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            pass


        except Exception as e:
            return jsonify({'message': 'Error fetching contract-product associations', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 500

@contract_product_bp.route('/ContractProducts/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def ContractProduct_id(id):
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