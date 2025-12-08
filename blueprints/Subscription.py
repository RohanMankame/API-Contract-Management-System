from flask import Blueprint, request, jsonify
from app import db
from models import Subscription, Subscription_tier
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.subscription_schema import subscription_read_schema, subscriptions_read_schema, subscription_write_schema
from schemas.subscription_tier_schema import subscription_tiers_read_schema
from marshmallow import ValidationError
from uuid import UUID

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

            new_subscription = Subscription(**validated, created_by=curr_user_id, updated_by=curr_user_id)
            db.session.add(new_subscription)
            db.session.commit()

            return jsonify({"message": "Subscription created successfully", "subscription": subscription_read_schema.dump(new_subscription)}), 201

        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": ve.messages}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 400

    elif request.method == 'GET':
        try:
            subscriptions = db.session.query(Subscription).all()
            
            return jsonify({"message": "Subscriptions fetched successfully","subscriptions": subscriptions_read_schema.dump(subscriptions)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Error fetching subscriptions"}), 400


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
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
            
            if not subscription:
                return jsonify({'error': 'Subscription not found'}), 404

            return jsonify({"message": "Subscription fetched successfully", "subscription": subscription_read_schema.dump(subscription)}), 200
        

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error getting subscription'}), 400
        

    elif request.method == 'PUT' or request.method == 'PATCH':
        try:
            data = request.get_json()
            
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
           

            if not subscription:
                return jsonify({'error': 'Subscription not found'}), 404
            
            validated = subscription_write_schema.load(data, partial=True)

            for key, value in validated.items():
                setattr(subscription, key, value)

            subscription.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'error': 'Subscription updated successfully'}), 200

        except ValidationError as ve:
            db.session.rollback()
            return jsonify({"error": "Validation error"}), 400

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error updating subscription'}), 500


    elif request.method == 'DELETE':
        try:
            id_obj = UUID(id) if isinstance(id, str) else id
            subscription = db.session.get(Subscription, id_obj)
            
            if not subscription:
                return jsonify({'error': 'Subscription not found'}), 404

            subscription.is_archived = True
            subscription.updated_by = curr_user_id
            db.session.commit()

            return jsonify({'message': 'Subscription has been archived successfully', "subscription": subscription_read_schema.dump(subscription)}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Error archiving subscription'}), 500


@subscription_bp.route('/Subscriptions/<id>/Tiers', methods=['GET'])
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
                return jsonify({'error': 'Subscription not found'}), 404

            tiers_objs = db.session.query(Subscription_tier).filter(Subscription_tier.subscription_id==id_obj).all()
            #tiers_objs = Subscription_tier.query.filter_by(subscription_id=id_obj, is_archived=False).all()
            tiers = subscription_tiers_read_schema.dump(tiers_objs)

            return jsonify({'tiers':tiers}), 200

        except Exception as e:
            return jsonify({'error': 'Error fetching subscription tiers', 'error': str(e)}), 500




