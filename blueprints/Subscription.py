from flask import Blueprint, request, jsonify
from app import db
from models import subscription
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.subscription_schema import subscription_read_schema, subscriptions_read_schema, subscription_write_schema
from marshmallow import ValidationError

# Initialize subscription Blueprint
subscription_bp = Blueprint('subscription', __name__)

# Subscription Endpoints


@subscription_bp.route('/Subscriptions', methods=['POST', 'GET'])
@jwt_required()
def Subscriptions():
    '''
    Post: Create a new subscription
    Get: Get all subscriptions from DB
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = subscription_write_schema.load(data)

            new_subscription = subscription(**validated,created_by=curr_user_id,updated_by=curr_user_id)

            db.session.add(new_subscription)
            db.session.commit()

            return jsonify(subscription=subscription_read_schema.dump(new_subscription)), 201

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400

    elif request.method == 'GET':
        try:
            subscriptions = subscription.query.all()
            return jsonify(subscriptions=subscriptions_read_schema.dump(subscriptions)), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400


@subscription_bp.route('/Subscriptions/<id>', methods=['GET','PUT','PATCH','DELETE'])
@jwt_required()
def Subscription_id(id):
    ''' 
    Get: Get details of specific Subscription
    Put: Update details of subscription with given ID
    Delete: Archive a subscription with given ID
    '''
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            subscription = subscription.query.get(id)
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            return jsonify(subscription=subscription_read_schema.dump(subscription)), 200

        except Exception as e:
            return jsonify({'message': 'Error getting subscription', 'error': str(e)}), 500
        

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            subscription = subscription.query.get(id)

            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404
            
            validated = subscription_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(subscription, key, value)

            subscription.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': 'Subscription updated successfully'}), 200

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({'message': 'Error updating subscription', 'error': str(e)}), 500


    elif request.method == 'DELETE':
        try:
            subscription = subscription.query.get(id)
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            subscription.is_archived = True
            subscription.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': 'Subscription has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving subscription', 'error': str(e)}), 500











"""
@subscription_bp.route('/Subscriptions/<id>/Tiers', methods=['GET'])
@jwt_required()
def Subscription_Tiers_id(id):
    '''
    Get: Get all tiers associated with a specific subscription
    '''
    if request.method == 'GET':
        try:
            subscription = Subscription.query.get(id)
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            tiers_list = []
            for tier in subscription.tiers:
                tiers_list.append({
                    'id': tier.id,
                    'subscription_id': tier.subscription_id,
                    'min_calls': tier.min_calls,
                    'max_calls': tier.max_calls,
                    'base_price': tier.base_price,
                    'price_per_tier': tier.price_per_tier,
                    'is_archived': tier.is_archived,
                })

            return jsonify(tiers_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching subscription tiers', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405

    """