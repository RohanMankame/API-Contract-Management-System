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
        # Logic to create a new product
        pass
    elif request.method == 'GET':
        # Logic to get all products
        pass



@product_bp.route('/Products/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def Product_id(id):
    ''' 
    Get: Get details of spefic Product(API)
    Put: Update details of product with given ID
    Delete: Delete product with given ID
    '''
    if request.method == 'GET':
        # Logic to get product details by ID
        pass

    elif request.method == 'PUT':
        # Logic to update product details by ID
        pass

    elif request.method == 'DELETE':
        # Logic to delete product by ID
        pass




@product_bp.route('/Products/<id>/Contracts', methods=['GET'])
@jwt_required()
def Product_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific product
    '''
    if request.method == 'GET':
        # Logic to get all contracts for a specific product
        pass
