from flask import Blueprint, request, jsonify
from app import db
from models import Product
from flask_jwt_extended import jwt_required, get_jwt_identity   

# Initialize product Blueprint
product_bp = Blueprint('product', __name__)

# Product Endpoints



"""
@product_bp.route('/Products', methods=['POST', 'GET'])
@jwt_required()
def Products():
    '''
    Post: Create a new API product
    Get: Get all API products from DB
    '''
    if request.method == 'POST':
        try:
            curr_user_id = get_jwt_identity()
            data = request.get_json()

            new_product = Product(
                api_name=data['api_name'],
                description=data['description'],
                is_archived=data.get('is_archived', False),
                created_by=curr_user_id,
                updated_by=curr_user_id
                )

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
    Delete: Archive a product with given ID
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
                'updated_at': product.updated_at,
                'created_by': product.created_by,
                'updated_by': product.updated_by
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

            if 'api_name' in data:
                product.api_name = data['api_name']
            if 'description' in data:
                product.description = data['description']
            if 'is_archived' in data:
                product.is_archived = data['is_archived']
            product.updated_by = get_jwt_identity()
            db.session.commit()

            return jsonify({'message': 'Product updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating product', 'error': str(e)}), 500

    elif request.method == 'DELETE':
        try:
            product = Product.query.get(id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            
            product.is_archived = True
            product.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Product has been archived successfully'}), 200
        
        except Exception as e:
            return jsonify({'message': 'Error archiving product', 'error': str(e)}), 500

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