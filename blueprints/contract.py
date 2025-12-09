from flask import Blueprint, request, jsonify
from app import db
from models import Contract, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.contract_schema import contract_read_schema, contracts_read_schema, contract_write_schema
from schemas.product_schema import product_read_schema, products_read_schema
from marshmallow import ValidationError
from uuid import UUID


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

            return jsonify({"message": "Contract created successfully", "contract": contract_read_schema.dump(new_contract)}), 201

        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500



    elif request.method == 'GET':
        try:
            contracts = db.session.query(Contract).all()
            
            return jsonify({"message": "Contracts fetched successfully", "contracts": contracts_read_schema.dump(contracts)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "An error occurred while fetching contracts"}), 500


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
            id_obj = UUID(id) if isinstance(id, str) else id
            contract = db.session.get(Contract, id_obj)
            
            if not contract:
                return jsonify({'error': 'Contract not found'}), 404

            return jsonify({"message": "Contract fetched successfully", "contract": contract_read_schema.dump(contract)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Error getting contract", "error": str(e)}), 500


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            id_obj = UUID(id) if isinstance(id, str) else id
            contract = db.session.get(Contract, id_obj)
            
            if not contract:
                return jsonify({"error": "Contract not found"}), 404

            is_partial = request.method == 'PATCH'
            validated = contract_write_schema.load(data, partial=is_partial) # changed partial=True to is_partial

            for key, value in validated.items():
                setattr(contract, key, value)

            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({"message": "Contract updated successfully", "contract": contract_read_schema.dump(contract)}), 200
        
        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error updating contract"}), 500


    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            contract = db.session.get(Contract, id_obj)
            
            if not contract:
                return jsonify({"error": "Contract not found"}), 404

            contract.is_archived = True
            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({"message": "Contract has been archived successfully"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error deleting contract"}), 500

    return jsonify({"error": "Method not allowed"}), 405


@contract_bp.route('/Contracts/<id>/Product', methods=['GET'])
@jwt_required()
def Contract_Product_id(id):
    '''
    Get: Get all products associated with a specific contract ID
    '''
    try:
        id_obj = UUID(id) if isinstance(id, str) else id
        contract = db.session.get(Contract, id_obj)
        
        if not contract:
            return jsonify({"error": "Contract not found"}), 404

        
        unique_products = {}
        for subscription in contract.subscriptions:
            
            product = subscription.product
            if not product:
                continue

            if getattr(product, "is_archived", False):
                continue

            unique_products[str(product.id)] = product

        products_list = products_read_schema.dump(list(unique_products.values()))
        return jsonify({"message": "Products fetched successfully", "products": products_list}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error getting products"}), 500
