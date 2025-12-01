from flask import Blueprint, request, jsonify
from app import db
from models import Product
from flask_jwt_extended import jwt_required, get_jwt_identity   
from schemas.product_schema import product_read_schema, products_read_schema, product_write_schema
from marshmallow import ValidationError

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

            new_product = Product(**validated,created_by=curr_user_id,updated_by=curr_user_id)

            db.session.add(new_product)
            db.session.commit()

            return jsonify(product=product_read_schema.dump(new_product)), 201
            
        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400
    


    elif request.method == 'GET':
        try:
            products = Product.query.all()
            return jsonify(products=products_read_schema.dump(products)), 200
        
        except Exception as e:
            return jsonify({"error": str(e)}), 400





@product_bp.route('/Products/<id>', methods=['GET','PUT', 'PATCH','DELETE'])
@jwt_required()
def Product_id(id):
    ''' 
    Get: Get details of spefic Product(API)
    Put/PATCH: Update details of product with given ID
    Delete: Archive a product with given ID
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            return jsonify(product=product_read_schema.dump(product)), 200

        except Exception as e:
            return jsonify({'message': 'Error getting product', 'error': str(e)}), 500



    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            validated = product_write_schema.load(data, partial=True)

            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            for key, value in validated.items():
                setattr(product, key, value)
            product.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': 'Product updated successfully'}), 200

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({'message': 'Error updating product', 'error': str(e)}), 500

            
    
    elif request.method == 'DELETE':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            product.is_archived = True
            product.updated_by = curr_user_id

            db.session.commit()
            return jsonify({'message': 'Product has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving product', 'error': str(e)}), 500




"""

@product_bp.route('/Products/<id>/Contracts', methods=['GET'])
@jwt_required()
def Product_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific product
    '''
    if request.method == 'GET':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            contracts_list = []
            seen_contracts = set()  
            
            for subscription in product.subscriptions:
                contract = subscription.contract
                
                # no duplicates
                if contract.id not in seen_contracts:
                    seen_contracts.add(contract.id)
                    
                    contracts_list.append({
                        'contract_id': str(contract.id),  
                        'client_id': str(contract.client_id), 
                        'contract_name': contract.contract_name,
                        'created_by': str(contract.created_by) if contract.created_by else None,  
                        'updated_by': str(contract.updated_by) if contract.updated_by else None,  
                        'created_at': contract.created_at.isoformat() if contract.created_at else None,
                        'updated_at': contract.updated_at.isoformat() if contract.updated_at else None,
                        'is_archived': contract.is_archived
                    })

            return jsonify({'contracts': contracts_list}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting contracts', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405

    """