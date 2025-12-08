from flask import Blueprint, request, jsonify
from app import db
from models import Product, Contract
from flask_jwt_extended import jwt_required, get_jwt_identity   
from schemas.product_schema import product_read_schema, products_read_schema, product_write_schema
from schemas.contract_schema import contracts_read_schema
from marshmallow import ValidationError
from uuid import UUID

# Initialize product Blueprint
product_bp = Blueprint('product', __name__)

# Product Endpoints

@product_bp.route('/Products', methods=['POST', 'GET'])
@jwt_required()
def Products():
    '''
    Post: Create a new API product
    Get: Get all API products from DB
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = product_write_schema.load(data)

            new_product = Product(**validated, created_by=curr_user_id, updated_by=curr_user_id)

            db.session.add(new_product)
            db.session.commit()

            return jsonify({"message": "Product created successfully", "product": product_read_schema.dump(new_product)}), 201
            
        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    


    elif request.method == 'GET':
        try:
            products = db.session.query(Product).all()
            
            return jsonify({"message": "Products retrieved successfully", "products": products_read_schema.dump(products)}), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500




@product_bp.route('/Products/<id>', methods=['GET','PUT', 'PATCH','DELETE'])
@jwt_required()
def Product_id(id):
    ''' 
    Get: Get details of spefic Product(API)
    Put/PATCH: Update details of product with given ID
    Get: Get details of specific Product(API)    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            return jsonify({"message": "Product retrieved successfully", "product": product_read_schema.dump(product)}), 200

        except Exception as e:
            return jsonify({'error': 'Error getting product', 'details': str(e)}), 500


    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            is_partial = request.method == 'PATCH'
            validated = product_write_schema.load(data, partial=is_partial)

            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return jsonify({'error': 'Product not found'}), 404
            
            if product.is_archived:
                return jsonify({'error': 'Cannot update an archived product'}), 400

            for key, value in validated.items():
                setattr(product, key, value)
            product.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': 'Product updated successfully', "product": product_read_schema.dump(product)}), 200

        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error updating product'}), 500

            
    
    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            product = db.session.get(Product, id_obj)
            
            if not product:
                return jsonify({'error': 'Product not found'}), 404

            product.is_archived = True
            product.updated_by = curr_user_id

            db.session.commit()
            return jsonify({'message': 'Product has been archived successfully', "product": product_read_schema.dump(product)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error archiving product', 'error': str(e)}), 500




@product_bp.route('/Products/<id>/Contracts', methods=['GET'])
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
                return jsonify({'error': 'Product not found'}), 404
           
            contracts_map = {}
            for subscription in product.subscriptions:
                cont = subscription.contract
                if cont and cont.id not in contracts_map:
                    contracts_map[cont.id] = cont

            contracts = list(contracts_map.values())
            return jsonify({"message": "Contracts retrieved successfully", "contracts": contracts_read_schema.dump(contracts)}), 200

        except Exception as e:
            return jsonify({'error': 'Error getting contracts', 'exception': str(e)}), 500
            



