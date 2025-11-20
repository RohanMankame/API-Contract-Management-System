from flask import Blueprint, request, jsonify
from app import db
from models import ContractProduct
from flask_jwt_extended import jwt_required

# Initialize contract_product Blueprint
contract_product_bp = Blueprint('contract_product', __name__)

# ContractProduct Endpoints
@contract_product_bp.route('/ContractProducts', methods=['POST', 'GET'])
#@jwt_required()
def ContractProducts():
    if request.method == 'POST':
        pass