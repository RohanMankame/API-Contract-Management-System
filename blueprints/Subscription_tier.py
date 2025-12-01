from flask import Blueprint, request, jsonify
from app import db
from models import Subscription_tier
from flask_jwt_extended import jwt_required, get_jwt_identity

subscription_tier_bp = Blueprint('subscription_tier', __name__)


@subscription_tier_bp.route('/Subscription_tiers', methods=['POST', 'GET'])
@jwt_required()
def Subscription_tiers():
    if request.method == 'POST':
        try:
            data = request.get_json()            

            new_tier = Subscription_tier(
                subscription_id = data['subscription_id'],
                min_calls = data['min_calls'],
                max_calls = data['max_calls'],
                start_date = data.get('start_date'),
                end_date = data.get('end_date'),
                base_price = data['base_price'],
                price_per_tier = data['price_per_tier'],
                is_archived = data.get('is_archived', False),
                created_by = get_jwt_identity(),
                updated_by = get_jwt_identity()
            )

            db.session.add(new_tier)
            db.session.commit()

            return jsonify({'message': 'Subscription tier created successfully', 'tier_id': new_tier.id}), 201
        
        except Exception as e:
            return jsonify({'message': 'Error creating subscription tier', 'error': str(e)}), 500



    elif request.method == 'GET':
        try:
            tiers = Subscription_tier.query.all()
            tiers_list = []

            for tier in tiers:
                tiers_list.append({
                    'id': tier.id,
                    'subscription_id': tier.subscription_id,
                    'min_calls': tier.min_calls,
                    'max_calls': tier.max_calls,
                    'start_date': tier.start_date,
                    'end_date': tier.end_date,
                    'base_price': tier.base_price,
                    'price_per_tier': tier.price_per_tier,
                    'is_archived': tier.is_archived,
                    'created_at': tier.created_at,
                    'updated_at': tier.updated_at,
                    'created_by': tier.created_by,
                    'updated_by': tier.updated_by
                })

            return jsonify(tiers_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching subscription tiers', 'error': str(e)}), 500

    return jsonify({'message': 'Invalid request method'}), 400


@subscription_tier_bp.route('/Subscription_tiers/<id>', methods=['GET','PUT','DELETE'])
@jwt_required()
def Subscription_tier_id(id):
    if request.method == 'GET':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            tier_data = {
                'id': tier.id,
                'subscription_id': tier.subscription_id,
                'min_calls': tier.min_calls,
                'max_calls': tier.max_calls,
                'start_date': tier.start_date,
                'end_date': tier.end_date,
                'price_per_tier': tier.price_per_tier,
            }

            return jsonify(tier_data), 200
        
        except Exception as e:
            return jsonify({'message': 'Error fetching subscription tier', 'error': str(e)}), 500


    elif request.method == 'PUT':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            data = request.get_json()
            tier.min_calls = data.get('min_calls', tier.min_calls)
            tier.max_calls = data.get('max_calls', tier.max_calls)
            tier.start_date = data.get('start_date', tier.start_date)
            tier.end_date = data.get('end_date', tier.end_date)
            tier.base_price = data.get('base_price', tier.base_price)
            tier.price_per_tier = data.get('price_per_tier', tier.price_per_tier)

            db.session.commit()

            return jsonify({'message': 'Subscription tier updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating subscription tier', 'error': str(e)}), 500


    elif request.method == 'DELETE':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            tier.is_archived = True
            tier.updated_by = get_jwt_identity()
            db.session.commit()

            return jsonify({'message': 'Subscription tier archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving subscription tier', 'error': str(e)}), 500



@subscription_tier_bp.route('/Subscription_tiers/<id>/Subscriptions', methods=['GET'])
@jwt_required()
def Subscription_tier_Subscriptions_id(id):
    if request.method == 'GET':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            subscription = tier.subscription  
            
            if not subscription:
                return jsonify({'message': 'No subscription found for this tier'}), 404

            subscription_data = {
                'id': str(subscription.id),
                'contract_id': str(subscription.contract_id),
                'product_id': str(subscription.product_id),
                'pricing_type': subscription.pricing_type,
                'strategy': subscription.strategy,
                'is_archived': subscription.is_archived,
                'created_at': subscription.created_at.isoformat(),
                'updated_at': subscription.updated_at.isoformat(),
                'created_by': str(subscription.created_by),
                'updated_by': str(subscription.updated_by)
            }

            return jsonify({'subscription': subscription_data}), 200
            
        except Exception as e:
            return jsonify({'message': 'Error fetching subscriptions for tier', 'error': str(e)}), 500

