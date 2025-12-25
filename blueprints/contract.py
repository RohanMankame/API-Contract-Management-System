from flask import Blueprint, request, jsonify
from app import db
from models import Contract, User
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.contract_schema import contract_read_schema, contracts_read_schema, contract_write_schema
from schemas.product_schema import product_read_schema, products_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error


# Initialize contract Blueprint
contract_bp = Blueprint('contract', __name__)

@contract_bp.route('/contracts', methods=['POST','GET'])
@jwt_required()
def Contracts():
    '''
    Post: Create a new contract
    Get: Get all contracts from DB
    '''
    current_user_id = get_jwt_identity()
    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = contract_write_schema.load(data)

            new_contract = Contract(**validated,created_by=current_user_id,updated_by=current_user_id)

            db.session.add(new_contract)
            db.session.commit()

            return created(data={"contract": contract_read_schema.dump(new_contract)}, message="Contract created successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error creating contract", errors=str(e))
        



    elif request.method == 'GET':
        try:
            contracts = db.session.query(Contract).filter_by(is_archived=False).all()
            
            return ok(data={"contracts": contracts_read_schema.dump(contracts)}, message="Contracts fetched successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error fetching contracts", errors=str(e))


@contract_bp.route('/contracts/<id>', methods=['GET', 'PUT','PATCH', 'DELETE'])
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
            contract = db.session.query(Contract).filter_by(id=id_obj, is_archived=False).first()
            
            if not contract:
                return not_found(message="Contract not found")

            return ok(data={"contract": contract_read_schema.dump(contract)}, message="Contract fetched successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error getting contract", errors=str(e))


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            id_obj = UUID(id) if isinstance(id, str) else id
            contract = db.session.get(Contract, id_obj)
            
            if not contract:
                return not_found(message="Contract not found")

            is_partial = request.method == 'PATCH'
            validated = contract_write_schema.load(data, partial=is_partial) 

            for key, value in validated.items():
                setattr(contract, key, value)

            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return ok(data={"contract": contract_read_schema.dump(contract)}, message="Contract updated successfully")
        
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error updating contract", errors=str(e))


    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            contract = db.session.get(Contract, id_obj)
            
            if not contract:
                return not_found(message="Contract not found")

            contract.is_archived = True
            contract.updated_by = get_jwt_identity()

            db.session.commit()
            return ok(message="Contract has been archived successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error deleting contract", errors=str(e))

    



@contract_bp.route('/contracts/<id>/product', methods=['GET'])
@jwt_required()
def Contract_Product_id(id):
    '''
    Get: Get all products associated with a specific contract ID
    '''
    try:
        id_obj = UUID(id) if isinstance(id, str) else id
        contract = db.session.get(Contract, id_obj)
        
        if not contract:
            return not_found(message="Contract not found")

        
        unique_products = {}
        for subscription in contract.subscriptions:
            
            product = subscription.product
            

            if getattr(product, "is_archived", False):
                continue 

            unique_products[str(product.id)] = product

        products_list = products_read_schema.dump(list(unique_products.values()))
        return ok(data={"products": products_list}, message="Products fetched successfully")

    except Exception as e:
        db.session.rollback()
        return server_error(message="Error getting products", errors=str(e))
