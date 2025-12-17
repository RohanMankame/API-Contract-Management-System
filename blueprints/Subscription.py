from flask import Blueprint, request
from app import db
from models import Subscription, SubscriptionTier 
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.subscription_schema import subscription_read_schema, subscriptions_read_schema, subscription_write_schema
from schemas.subscription_tier_schema import subscription_tiers_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

# Initialize subscription Blueprint
subscription_bp = Blueprint('subscription', __name__)

# Subscription Endpoints
@subscription_bp.route('/subscriptions', methods=['POST', 'GET'])
@jwt_required()
def Subscriptions():
    '''
    Post: Create a new subscription
    Get: Get all subscriptions from DB
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = subscription_write_schema.load(data)

            new_subscription = Subscription(**validated, created_by=current_user_id, updated_by=current_user_id)
            db.session.add(new_subscription)
            db.session.commit()

            return created(data={"subscription": subscription_read_schema.dump(new_subscription)}, message="Subscription created successfully")


        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error creating subscription", errors=str(e))

    elif request.method == 'GET':
        try:
            subscriptions = db.session.query(Subscription).all()
        
            return ok(data={"subscriptions": subscriptions_read_schema.dump(subscriptions)}, message="Subscriptions fetched successfully")


        except Exception as e:
            db.session.rollback()
            return server_error(message="Error fetching subscriptions", errors=str(e))


@subscription_bp.route('/subscriptions/<id>', methods=['GET','PUT','PATCH','DELETE'])
@jwt_required()
def Subscription_id(id):
    ''' 
    Get: Get details of specific Subscription
    Put: Update details of subscription with given ID
    Delete: Archive a subscription with given ID
    '''
    current_user_id = get_jwt_identity()

    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
            
            if not subscription:
                return not_found(message="Subscription not found")

            return ok(data={"subscription": subscription_read_schema.dump(subscription)}, message="Subscription fetched successfully")
        

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error getting subscription")
        

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
           

            if not subscription:
                return not_found(message="Subscription not found")
            
            validated = subscription_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(subscription, key, value)

            subscription.updated_by = current_user_id
            db.session.commit()

            return ok(data={"subscription": subscription_read_schema.dump(subscription)}, message="Subscription updated successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error updating subscription", errors=str(e))


    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
            
            if not subscription:
                return not_found(message="Subscription not found")

            subscription.is_archived = True
            subscription.updated_by = current_user_id
            db.session.commit()

            return ok(data={"subscription": subscription_read_schema.dump(subscription)}, message="Subscription has been archived successfully")    

        except Exception as e:
            db.session.rollback()
            return server_error(message="Error archiving subscription", errors=str(e))


@subscription_bp.route('/subscriptions/<id>/tiers', methods=['GET'])
@jwt_required()
def Subscription_Tiers_id(id):
    '''
    Get: Get all tiers associated with a specific subscription
    '''
    if request.method == 'GET':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
            
            if not subscription:
                return not_found(message="Subscription not found") 

            tiers_objs = db.session.query(SubscriptionTier).filter(SubscriptionTier.subscription_id==id_obj).all()
            tiers = subscription_tiers_read_schema.dump(tiers_objs)

            return ok(data={"tiers": tiers}, message="Subscription tiers fetched successfully")

        except Exception as e:
            return server_error(message="Error fetching subscription tiers", errors=str(e))




