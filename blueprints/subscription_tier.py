from flask import Blueprint, request
from app import db
from models import SubscriptionTier 
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.subscription_tier_schema import subscription_tier_read_schema, subscription_tiers_read_schema, subscription_tier_write_schema
from schemas.subscription_schema import subscription_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

subscription_tier_bp = Blueprint('subscription_tier', __name__)

@subscription_tier_bp.route('/subscription-tiers', methods=['POST', 'GET'])
@jwt_required()
def Subscription_tier():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = subscription_tier_write_schema.load(data)

            new_tier = SubscriptionTier(**validated, created_by=current_user_id, updated_by=current_user_id)

            db.session.add(new_tier)
            db.session.commit()
            return created(data={"subscription_tier": subscription_tier_read_schema.dump(new_tier)}, message="Subscription tier created successfully")
        
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)
        
        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error creating subscription tier: {e}")
    
    elif request.method == 'GET':
        try:
            tiers = db.session.query(SubscriptionTier).filter_by(is_archived=False).all()
            
            return ok(data={"subscription_tiers": subscription_tiers_read_schema.dump(tiers)}, message="Subscription tiers retrieved successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error fetching subscription tiers: {e}")


@subscription_tier_bp.route('/subscription-tiers/<id>', methods=['GET','PUT','PATCH','DELETE'])
@jwt_required()
def Subscription_tier_id(id):
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            tier = db.session.query(SubscriptionTier).filter_by(id=id_obj, is_archived=False).first()
            
            if not tier:
                return not_found(message="Subscription tier not found")

            return ok(data={"subscription_tier": subscription_tier_read_schema.dump(tier)}, message="Subscription tier retrieved successfully")
        
        except ValidationError as ve:
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            return server_error(message=f"Error getting subscription tier: {e}")

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            id_obj = UUID(id) if isinstance(id, str) else id
            tier = db.session.get(SubscriptionTier, id_obj)
            
            if not tier:
                return not_found(message="Subscription tier not found")

            validated = subscription_tier_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(tier, key, value)
            tier.updated_by = current_user_id

            db.session.commit()
            return ok(data={"subscription_tier": subscription_tier_read_schema.dump(tier)}, message="Subscription tier updated successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)
        
        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error updating subscription tier: {e}")

    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            tier = db.session.get(SubscriptionTier, id_obj)
            
            if not tier:
                return not_found(message="Subscription tier not found")

            tier.is_archived = True
            tier.updated_by = current_user_id

            db.session.commit()
            return ok(data={"subscription_tier": subscription_tier_read_schema.dump(tier)}, message="Subscription tier archived successfully")
        
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error archiving subscription tier: {e}")
        

@subscription_tier_bp.route('/subscription-tiers/<id>/subscriptions', methods=['GET'])
@jwt_required()
def Subscription_tier_Subscriptions_id(id):
    '''
    Get: Get the subscription associated with a specific subscription tier ID
    '''
    try:
        id_obj = UUID(id) if isinstance(id, str) else id
        tier = db.session.get(SubscriptionTier, id_obj)
        
        if not tier:
            return not_found(message="Subscription tier not found")

        subscription = getattr(tier, 'subscription', None)
        if not subscription:
            return not_found(message="No subscription found for this tier")

        subscription_data = subscription_read_schema.dump(subscription)
        return ok(data={'subscription': subscription_data}, message="Subscription retrieved successfully")

    except Exception as e:
        db.session.rollback()
        return server_error(message=f"Error fetching subscriptions for tier: {e}")