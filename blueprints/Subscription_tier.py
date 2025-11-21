from flask import Blueprint, request, jsonify
from app import db
from models import Subscription_tier
from flask_jwt_extended import jwt_required

Subscription_tier_bp = Blueprint('subscription_tier', __name__)


@Subscription_tier_bp.route('/Subscription_tiers', methods=['POST', 'GET'])
#@jwt_required()
def Subscription_tiers():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        pass




@Subscription_tier_bp.route('/Subscription_tiers/<id>', methods=['GET','PUT','DELETE'])
#@jwt_required()
def Subscription_tier_id(id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass



@Subscription_tier_bp.route('/Subscription_tiers/<id>/Subscriptions', methods=['GET'])
#@jwt_required()
def Subscription_tier_Subscriptions_id(id):
    if request.method == 'GET':
        pass

