from flask import Blueprint, request, jsonify
from app import db
from models import Subscription
from flask_jwt_extended import jwt_required, get_jwt_identity


Subscription_bp = Blueprint('subscription', __name__)

@Subscription_bp.route('/Subscriptions', methods=['POST', 'GET'])
@jwt_required()
def Subscriptions():
    '''
    Post: Create a new subscription
    Get: Get all subscriptions from DB
    '''
    if request.method == 'POST':
        try:
            data = request.get_json()

            new_subscription = Subscription(
                contract_id = data['contract_id'],
                product_id = data['product_id'],
                pricing_type = data['pricing_type'],
                strategy = data['strategy'],
                is_archived = data.get('is_archived', False),
                created_by = get_jwt_identity(),
                updated_by = get_jwt_identity()
            )

            db.session.add(new_subscription)
            db.session.commit()

            return jsonify({'message': 'Subscription created successfully', 'subscription_id': new_subscription.id}), 201

        except Exception as e:
            return jsonify({'message': 'Error creating subscription', 'error': str(e)}), 500


    elif request.method == 'GET':
        try:
            subscriptions = Subscription.query.all()
            subscriptions_list = []

            for subscription in subscriptions:
                subscriptions_list.append({
                    'id': subscription.id,
                    'contract_id': subscription.contract_id,
                    'product_id': subscription.product_id,
                    'princing_type': subscription.pricing_type,
                    'strategy': subscription.strategy,
                    'is_archived': subscription.is_archived,
                    'created_at': subscription.created_at,
                    'updated_at': subscription.updated_at,
                    'created_by': subscription.created_by,
                    'updated_by': subscription.updated_by
                })

            return jsonify(subscriptions_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching subscriptions', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 400


@Subscription_bp.route('/Subscriptions/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def Subscription_id(id):
    ''' 
    Get: Get details of specific Subscription
    Put: Update details of subscription with given ID
    Delete: Archive a subscription with given ID
    '''
    if request.method == 'GET':
        try:
            subscription = Subscription.query.get(id)
            
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            subscription_data = {
                    'id': subscription.id,
                    'contract_id': subscription.contract_id,
                    'product_id': subscription.product_id,
                    'princing_type': subscription.pricing_type,
                    'strategy': subscription.strategy,
                    'is_archived': subscription.is_archived,
                    'created_at': subscription.created_at,
                    'updated_at': subscription.updated_at,
                    'created_by': subscription.created_by,
                    'updated_by': subscription.updated_by
            }

            return jsonify(subscription_data), 200

        except Exception as e:
            return jsonify({'message': 'Error getting subscription', 'error': str(e)}), 500
        

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            subscription = Subscription.query.get(id)

            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404
            
            if 'contract_id' in data:
                subscription.contract_id = data['contract_id']
            if 'product_id' in data:
                subscription.product_id = data['product_id']
            if 'pricing_type' in data:
                subscription.pricing_type = data['pricing_type']
            if 'strategy' in data:
                subscription.strategy = data['strategy']
            if 'is_archived' in data:
                subscription.is_archived = data['is_archived']

            subscription.updated_by = get_jwt_identity()
            db.session.commit()

            return jsonify({'message': 'Subscription updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating subscription', 'error': str(e)}), 500


    elif request.method == 'DELETE':
        try:
            subscription = Subscription.query.get(id)
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            subscription.is_archived = True
            subscription.updated_by = get_jwt_identity()
            db.session.commit()

            return jsonify({'message': 'Subscription has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving subscription', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405


@Subscription_bp.route('/Subscriptions/<id>/Tiers', methods=['GET'])
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