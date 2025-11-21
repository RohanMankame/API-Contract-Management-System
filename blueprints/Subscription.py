from flask import Blueprint, request, jsonify
from app import db
from models import Subscription
from flask_jwt_extended import jwt_required


Subscription_bp = Blueprint('subscription', __name__)

@Subscription_bp.route('/Subscriptions', methods=['POST', 'GET'])
#@jwt_required()
def Subscriptions():
    '''
    Post: Create a new subscription
    Get: Get all subscriptions from DB
    '''
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass


@Subscription_bp.route('/Subscriptions/<id>', methods=['GET','PUT','DELETE'])
#@jwt_required()
def Subscription_id(id):
    ''' 
    Get: Get details of specific Subscription
    Put: Update details of subscription with given ID
    Delete: Delete subscription with given ID
    '''
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass


@Subscription_bp.route('/Subscriptions/<id>/Tiers', methods=['GET'])
#@jwt_required()
def Subscription_Tiers_id(id):
    '''
    Get: Get all tiers associated with a specific subscription
    '''
    if request.method == 'GET':
        pass