from flask import Blueprint, request, jsonify
from app import db
from models import Subscription_tier
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.subscription_tier_schema import subscription_tier_read_schema, subscription_tiers_read_schema, subscription_tier_write_schema
from marshmallow import ValidationError

subscription_tier_bp = Blueprint('subscription_tier', __name__)


@subscription_tier_bp.route('/Subscription_tiers', methods=['POST', 'GET'])
@jwt_required()
def Subscription_tiers():
    curr_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = subscription_tier_write_schema.load(data)

            new_tier = Subscription_tier(**validated,created_by=curr_user_id,updated_by=curr_user_id)

            db.session.add(new_tier)
            db.session.commit()

            return jsonify(subscription_tier=subscription_tier_read_schema.dump(new_tier)), 201

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    
    elif request.method == 'GET':
        try:
            tiers = Subscription_tier.query.all()
            return jsonify(subscription_tiers=subscription_tiers_read_schema.dump(tiers)), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 400



@subscription_tier_bp.route('/Subscription_tiers/<id>', methods=['GET','PUT','PATCH','DELETE'])
@jwt_required()
def Subscription_tier_id(id):
    curr_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            return jsonify(subscription_tier=subscription_tier_read_schema.dump(tier)), 200
        
        except Exception as e:
            return jsonify({'message': 'Error fetching subscription tier', 'error': str(e)}), 500
    



    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            validated = subscription_tier_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(tier, key, value)
            tier.updated_by = curr_user_id

            db.session.commit()

            return jsonify({'message': 'Subscription tier updated successfully'}), 200

        except ValidationError as ve:
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            return jsonify({'message': 'Error updating subscription tier', 'error': str(e)}), 500




    elif request.method == 'DELETE':
        try:
            tier = Subscription_tier.query.get(id)
            if not tier:
                return jsonify({'message': 'Subscription tier not found'}), 404

            tier.is_archived = True
            tier.updated_by = curr_user_id

            db.session.commit()
            return jsonify({'message': 'Subscription tier archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error archiving subscription tier', 'error': str(e)}), 500





@subscription_tier_bp.route('/Subscription_tiers/<id>/Subscriptions', methods=['GET'])
@jwt_required()
def Subscription_tier_Subscriptions_id(id):
    """
    GET: Get subscriptions associated with a specific subscription tier using tier ID
    """
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




