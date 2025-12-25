from flask import Blueprint, request, jsonify
from app import db
from models import Product, Contract
from flask_jwt_extended import jwt_required, get_jwt_identity   
from schemas.product_schema import product_read_schema, products_read_schema, product_write_schema
from schemas.contract_schema import contracts_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

# Initialize product Blueprint
product_bp = Blueprint('product', __name__)

# Product Endpoints
@product_bp.route('/products', methods=['POST', 'GET'])
@jwt_required()
def Products():
    '''
    Post: Create a new API product
    Get: Get all API products from DB
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = product_write_schema.load(data)

            new_product = Product(**validated, created_by=current_user_id, updated_by=current_user_id)

            db.session.add(new_product)
            db.session.commit()

            return created(data={"product": product_read_schema.dump(new_product)}, message="Product created successfully")
            
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)
        

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error creating product", errors=str(e))


    elif request.method == 'GET':
        try:
            products = db.session.query(Product).filter_by(is_archived=False).all()
        
            return ok(data={"products": products_read_schema.dump(products)}, message="Products retrieved successfully")

        except Exception as e:
            return server_error(message="Error fetching products", errors=str(e))


@product_bp.route('/products/<id>', methods=['GET','PUT', 'PATCH','DELETE'])
@jwt_required()
def Product_id(id):
    ''' 
    Get: Get details of spefic Product(API)
    Put/PATCH: Update details of product with given ID
    Get: Get details of specific Product(API)    '''
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.query(Product).filter_by(id=id_obj, is_archived=False).first()
            
            if not product:
                return not_found(message="Product not found")

            return ok(data={"product": product_read_schema.dump(product)}, message="Product retrieved successfully")
        
        except Exception as e:
            return server_error(message="Error getting product", errors=str(e))


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            is_partial = request.method == 'PATCH'
            validated = product_write_schema.load(data, partial=is_partial)

            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return not_found(message="Product not found")
            
            if product.is_archived:
                return bad_request(message="Cannot update an archived product")

            for key, value in validated.items():
                setattr(product, key, value)
            product.updated_by = current_user_id
            db.session.commit()

            return ok(data={"product": product_read_schema.dump(product)}, message="Product updated successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error updating product", errors=str(e))

            
    
    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return not_found(message="Product not found")

            product.is_archived = True
            product.updated_by = current_user_id

            db.session.commit()
            return ok(data={"product": product_read_schema.dump(product)}, message="Product has been archived successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error archiving product", errors=str(e))



@product_bp.route('/products/<id>/contracts', methods=['GET'])
@jwt_required()
def Product_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific product
    '''
    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return not_found(message="Product not found")
           
            contracts_map = {}
            for subscription in product.subscriptions:
                cont = subscription.contract
                if cont and cont.id not in contracts_map:
                    contracts_map[cont.id] = cont

            contracts = list(contracts_map.values())
            return ok(data={"contracts": contracts_read_schema.dump(contracts)}, message="Contracts retrieved successfully")

        except Exception as e:
            return server_error(message="Error getting contracts", errors=str(e))
            



