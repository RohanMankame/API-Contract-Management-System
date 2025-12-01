from flask import Blueprint, request, jsonify
from app import db
from models import Contract, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.contract_schema import contract_read_schema, contracts_read_schema, contract_write_schema
from marshmallow import ValidationError
from utils.serializer import serialize_contract

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
    curr_user_id = get_jwt_identity()
    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = contract_write_schema.load(data)

            new_contract = Contract(**validated,created_by=curr_user_id,updated_by=curr_user_id)

            db.session.add(new_contract)
            db.session.commit()

            return jsonify(contract=contract_read_schema.dump(new_contract)), 201

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400



    elif request.method == 'GET':
        try:
            contracts = Contract.query.all()
            return jsonify(contracts=contracts_read_schema.dump(contracts)), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


@contract_bp.route('/Contracts/<id>', methods=['GET', 'PUT','PATCH', 'DELETE'])
@jwt_required()
def Contract_id(id):
    ''' 
    Get: Get details of specific Contract
    Put/PATCH: Update details of contract with given ID
    Delete: Archive a contract with given ID
    '''
    if request.method == 'GET':
        try:
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            return jsonify(contract=contract_read_schema.dump(contract)), 200

        except Exception as e:
            return jsonify({'message': 'Error getting contract', 'error': str(e)}), 500


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            contract = Contract.query.get(id)
            if not contract:
                return jsonify({'message': 'Contract not found'}), 404

            validated = contract_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(contract, key, value)

            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Contract updated successfully'}), 200

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

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

        unique_products = {}
    
        for subscription in contract.subscriptions:

            product = subscription.product
            if product.id not in unique_products:
                unique_products[product.id] = {
                    'id': str(product.id),
                    'api_name': product.api_name,  
                    'description': product.description,
                    'is_archived': product.is_archived,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat(),
                    'created_by': str(product.created_by),
                    'updated_by': str(product.updated_by)
                }

        return jsonify({'products': list(unique_products.values())}), 200
    
    
    except Exception as e:
        return jsonify({'message': 'Error getting products', 'error': str(e)}), 500

