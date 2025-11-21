from flask import Blueprint, request, jsonify
from app import db
from models import Product
from flask_jwt_extended import jwt_required

# Initialize product Blueprint
product_bp = Blueprint('product', __name__)

# Product Endpoints

@product_bp.route('/Products', methods=['POST', 'GET'])
#@jwt_required()
def Products():
    '''
    Post: Create a new API product
    Get: Get all API products from DB
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()
            api_name = data['api_name']
            description = data['description']
            is_archived = data.get('is_archived', False)

            new_product = Product(
                api_name=api_name,
                description=description,
                is_archived=is_archived)

            db.session.add(new_product)
            db.session.commit()
            return jsonify({'message': 'Product created successfully', 'product_id': new_product.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating product', 'error': str(e)}), 500
        
    elif request.method == 'GET':
        try:
            products = Product.query.all()
            products_list = []

            for product in products:
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
            return jsonify({'message': 'Error getting products', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405


@product_bp.route('/Products/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def Product_id(id):
    ''' 
    Get: Get details of spefic Product(API)
    Put: Update details of product with given ID
    Delete: Delete product with given ID
    '''
    if request.method == 'GET':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404

            product_data = {
                'id': product.id,
                'api_name': product.api_name,
                'description': product.description,
                'is_archived': product.is_archived,
                'created_at': product.created_at,
                'updated_at': product.updated_at
            }

            return jsonify({'product': product_data}), 200

        except Exception as e:
            return jsonify({'message': 'Error getting product', 'error': str(e)}), 500



    elif request.method == 'PUT':
        try:
            data = request.get_json()
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            product.api_name = data['api_name']
            product.description = data['description']
            product.is_archived = data.get('is_archived', product.is_archived)
            db.session.commit()
            return jsonify({'message': 'Product updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating product', 'error': str(e)}), 500



    elif request.method == 'DELETE':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': 'Error deleting product', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405





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
            for subscription in product.subscriptions:
                contract = subscription.contract
                contracts_list.append({
                    'contract_id': contract.id,
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