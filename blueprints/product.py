from flask import Blueprint, request, jsonify
from app import db
from models import Product
from flask_jwt_extended import jwt_required

# Initialize product Blueprint
product_bp = Blueprint('product', __name__)

# Product Endpoints

@product_bp.route('/createProduct', methods=['POST'])
@jwt_required()
def createProduct():
    '''
    create a new API product and add to DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send product details in JSON format"}, 400

    data = request.get_json()

    try:
        product = Product(
            name=data.get('name'),
            version=data.get('version'),
            pricing_type=data.get('pricing_type'),
            price_per_month=float(data.get('price', 0.0)),
            calls_per_month=int(data.get('calls_per_month', 0)),
            call_limit_type=int(data.get('call_limit_type'))
        )

        db.session.add(product)
        db.session.commit()
        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400




@product_bp.route('/getProducts', methods=['GET'])
@jwt_required()
def getProducts():
    '''
    Get all API products from DB
    '''
    try:
        products = Product.query.all()
        products_list = [{
            "id": product.id,
            "name": product.name,
            "version": product.version,
            "pricing_type": product.pricing_type,
            "price_per_month": product.price_per_month,
            "calls_per_month": product.calls_per_month,
            "call_limit_type": product.call_limit_type
        } for product in products]
        return {"products": products_list}, 200

    except Exception as e:
        return {"error getProds": str(e)}, 400





@product_bp.route('/getProduct/<productID>',methods=['GET'])
@jwt_required()
def getProductByID(productID):
    '''
    Get existing API product from DB using product ID
    '''
    try:
        product = Product.query.get(productID)
        if product:
            return {
                "id": product.id,
                "name": product.name,
                "version": product.version,
                "pricing_type": product.pricing_type,
                "price_per_month": product.price_per_month,
                "calls_per_month": product.calls_per_month,
                "call_limit_type": product.call_limit_type
            }, 200
        else:
            return {"error": "Product not found"}, 404

    except Exception as e:
        return {"error": str(e)}, 400





@product_bp.route('/updateProduct/<productID>', methods=['PUT'])
@jwt_required()
def updateProductByID(productID):
    '''
    Update existing API product in DB using product ID
    '''
    try:
        product = Product.query.get(productID)
        if not product:
            return {"error": "Product not found"}, 404

        if not request.is_json:
            return {"error": "Invalid input, send product details in JSON format"}, 400

        data = request.get_json()

        product.name = data.get('name', product.name)
        product.version = data.get('version', product.version)
        product.pricing_type = data.get('pricing_type', product.pricing_type)
        product.price_per_month = float(data.get('price_per_month', product.price_per_month))
        product.calls_per_month = int(data.get('calls_per_month', product.calls_per_month))
        product.call_limit_type = int(data.get('call_limit_type', product.call_limit_type))

        db.session.commit()
        return {"message": "Product updated"}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400




@product_bp.route('/deleteProduct/<productID>', methods=['DELETE'])
@jwt_required()
def deleteProductByID(productID):
    '''
    Delete existing API product from DB using product ID
    '''
    try:
        product = Product.query.get(productID)
        if not product:
            return {"error": "Product not found"}, 404

        db.session.delete(product)
        db.session.commit()
        return {"message": "Product deleted"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400