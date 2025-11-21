from flask import Blueprint, request, jsonify, make_response
from app import db
from models import User
import validators
from flask_jwt_extended import jwt_required

# Initialize user Blueprint
user_bp = Blueprint('user', __name__)

# User Endpoints

@user_bp.route('/Users', methods=['POST','GET'])
#@jwt_required()
def Users():
    '''
    Post: Create a new user
    Get: Get all users from DB
    '''
    pass
    


@user_bp.route('/Users/<id>', methods=['GET', 'PUT', 'DELETE'])
#@jwt_required()
def User_id(id):
    '''
    GET: Get existing user from DB using user ID
    PUT: Update existing user in DB using user ID
    DELETE: Delete existing user from DB using user ID
    '''
    pass
    

@user_bp.route('/Users/<id>/Contracts', methods=['GET'])
@jwt_required()
def User_Contracts_id(id):
    '''
    Get: Get all contracts associated with a specific user
    '''
    pass