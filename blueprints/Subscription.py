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
        try:
            data = request.get_json()
            contract_id = data['contract_id']
            product_id = data['product_id']
            start_date = data['start_date']
            end_date = data['end_date']
            pricing_type = data['pricing_type']
            varible_strategy = data.get('varible_strategy', None)
            base_price = data['base_price']
            is_archived = data.get('is_archived', False)

            new_subscription = Subscription(
                contract_id=contract_id,
                product_id=product_id,
                start_date=start_date,
                end_date=end_date,
                pricing_type=pricing_type,
                varible_strategy=varible_strategy,
                base_price=base_price,
                is_archived=is_archived
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
                    'start_date': subscription.start_date,
                    'end_date': subscription.end_date,
                    'pricing_type': subscription.pricing_type,
                    'varible_strategy': subscription.varible_strategy,
                    'base_price': subscription.base_price,
                    'is_archived': subscription.is_archived
                })

            return jsonify(subscriptions_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching subscriptions', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 400


@Subscription_bp.route('/Subscriptions/<id>', methods=['GET','PUT','DELETE'])
#@jwt_required()
def Subscription_id(id):
    ''' 
    Get: Get details of specific Subscription
    Put: Update details of subscription with given ID
    Delete: Delete subscription with given ID
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
                'start_date': subscription.start_date,
                'end_date': subscription.end_date,
                'pricing_type': subscription.pricing_type,
                'varible_strategy': subscription.varible_strategy,
                'base_price': subscription.base_price,
                'is_archived': subscription.is_archived
            }

            return jsonify(subscription_data), 200

        except Exception as e:
            return jsonify({'message': 'Error getting subscription', 'error': str(e)}), 500
        

    elif request.method == 'PUT':
        try:
            subscription = Subscription.query.get(id)
            if not subscription:
                return jsonify({'message': 'Subscription not found'}), 404

            data = request.get_json()
            subscription.contract_id = data.get('contract_id', subscription.contract_id)
            subscription.product_id = data.get('product_id', subscription.product_id)
            subscription.start_date = data.get('start_date', subscription.start_date)
            subscription.end_date = data.get('end_date', subscription.end_date)
            subscription.pricing_type = data.get('pricing_type', subscription.pricing_type)
            subscription.varible_strategy = data.get('varible_strategy', subscription.varible_strategy)
            subscription.base_price = data.get('base_price', subscription.base_price)
            subscription.is_archived = data.get('is_archived', subscription.is_archived)

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
            db.session.commit()

            return jsonify({'message': 'Subscription has been archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving subscription', 'error': str(e)}), 500

    return jsonify({'message': 'Method not allowed'}), 405


@Subscription_bp.route('/Subscriptions/<id>/Tiers', methods=['GET'])
#@jwt_required()
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
            for tier in subscription.subscription_tiers:
                tiers_list.append({
                    'id': tier.id,
                    'subscription_id': tier.subscription_id,
                    'tier_name': tier.tier_name,
                    'min_calls': tier.min_calls,
                    'max_calls': tier.max_calls,
                    'price_per_tier': tier.price_per_tier,
                })

            return jsonify(tiers_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching subscription tiers', 'error': str(e)}), 500
    
    return jsonify({'message': 'Method not allowed'}), 405