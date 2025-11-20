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

            # Validate input
            if not data.get('name') or not data.get('version'):
                return jsonify({'message': 'Missing required fields'}), 400

            # Check for existing product
            if Product.query.filter_by(name=data['name']).first():
                return jsonify({'message': 'Product with given name already exists'}), 409

            # Create new product
            new_product = Product(
                name=data['name'],
                version=data['version']
            )

            db.session.add(new_product)
            db.session.commit()

            return jsonify({'message': 'Product created successfully', 'product_id': new_product.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating product', 'error': str(e)}), 500

    elif request.method == 'GET':
        try:
            products = Product.query.all()
            products_list = [{'id': product.id, 'name': product.name, 'version': product.version} for product in products]
            return jsonify(products_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching products', 'error': str(e)}), 500


@product_bp.route('/Products/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def Product_id():
    ''' 
    Get: Get details of spefic Product(API)
    Put: Update details of product with given ID
    Delete: Delete product with given ID
    '''
    pass




@product_bp.route('/Products/<id>/Contracts', methods=['GET'])
@jwt_required()
def Product_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific product
    '''
    pass