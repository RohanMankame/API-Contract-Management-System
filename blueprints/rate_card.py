from flask import Blueprint, request
from app import db
from models import RateCard, SubscriptionTier
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.rate_card_schema import rate_card_read_schema, rate_cards_read_schema, rate_card_write_schema
from schemas.subscription_tier_schema import subscription_tiers_read_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

rate_card_bp = Blueprint('rate_card', __name__)

def _parse_uuid(val):
    """Accept both str and uuid.UUID; raise ValueError on invalid."""
    if isinstance(val, UUID):
        return val
    if isinstance(val, str):
        return UUID(val)
    raise ValueError("Invalid UUID value")

@rate_card_bp.route('/rate-cards', methods=['POST', 'GET'])
@jwt_required()
def Rate_card():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json() or {}
            rate_card_write_schema.context = {"current_rate_card_id": None}
            validated = rate_card_write_schema.load(data)

            new_rate_card = RateCard(**validated, created_by=current_user_id, updated_by=current_user_id)

            db.session.add(new_rate_card)
            db.session.commit()
            return created(data={"rate_card": rate_card_read_schema.dump(new_rate_card)}, message="Rate card created successfully")
        
        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error creating rate card: {e}")
    
    elif request.method == 'GET':
        try:
            rate_cards = db.session.query(RateCard).filter_by(is_archived=False).all()
            return ok(data={"rate_cards": rate_cards_read_schema.dump(rate_cards)}, message="Rate cards retrieved successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error fetching rate cards: {e}")
        

@rate_card_bp.route('/rate-cards/<id>', methods=['GET','PUT','PATCH','DELETE'])
@jwt_required()
def Rate_card_id(id):
    current_user_id = get_jwt_identity()

    try:
        id_obj = _parse_uuid(id) if isinstance(id, str) else id
    except Exception:
        return bad_request(message="Invalid rate card id format", errors={"id": "Invalid UUID format"})

    if request.method == 'GET':
        try:
            rate_card_item = db.session.get(RateCard, id_obj)
            if not rate_card_item or rate_card_item.is_archived:
                return not_found(message="Rate card not found")

            return ok(data={"rate_card": rate_card_read_schema.dump(rate_card_item)}, message="Rate card retrieved successfully")
        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error fetching rate card: {e}")
        
    elif request.method in ['PUT', 'PATCH']:
        try:
            rate_card_item = db.session.get(RateCard, id_obj)
            if not rate_card_item or rate_card_item.is_archived:
                return not_found(message="Rate card not found")

            data = request.get_json() or {}
            #validated = rate_card_write_schema.load(data, partial=(request.method == 'PATCH'))

            # Set context on schema instance
            rate_card_write_schema.context = {"current_rate_card_id": id_obj}
            validated = rate_card_write_schema.load(data, partial=(request.method == 'PATCH'))

            for key, value in validated.items():
                setattr(rate_card_item, key, value)
            rate_card_item.updated_by = current_user_id

            db.session.commit()
            return ok(data={"rate_card": rate_card_read_schema.dump(rate_card_item)}, message="Rate card updated successfully")

        except ValidationError as ve:
            db.session.rollback()
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error updating rate card: {e}")

    elif request.method == 'DELETE':
        try:
            rate_card_item = db.session.get(RateCard, id_obj)
            if not rate_card_item or rate_card_item.is_archived:
                return not_found(message="Rate card not found")

            # soft-archive
            rate_card_item.is_archived = True
            rate_card_item.updated_by = current_user_id

            # cascade archive tiers in bulk for performance
            db.session.query(SubscriptionTier)\
                .filter(SubscriptionTier.rate_card_id == rate_card_item.id, SubscriptionTier.is_archived == False)\
                .update({"is_archived": True, "updated_by": current_user_id}, synchronize_session=False)

            db.session.commit()
            return ok(message="Rate card archived successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error archiving rate card: {e}")
        

@rate_card_bp.route('/rate-cards/<id>/subscription-tiers', methods=['GET'])
@jwt_required()
def Rate_card_subscription_tiers(id):
    try:
        id_obj = _parse_uuid(id) if isinstance(id, str) else id
    except Exception:
        return bad_request(message="Invalid rate card id format", errors={"id": "Invalid UUID format"})

    try:
        rate_card_item = db.session.get(RateCard, id_obj)
        if not rate_card_item or rate_card_item.is_archived:
            return not_found(message="Rate card not found")

        # Query tiers associated with this rate card (DB-side)
        tiers = db.session.query(SubscriptionTier).filter_by(rate_card_id=id_obj, is_archived=False).all()

        return ok(data={"subscription_tiers": subscription_tiers_read_schema.dump(tiers)}, message=f"Subscription tiers for id:{id} retrieved successfully")

    except Exception as e:
        db.session.rollback()
        return server_error(message=f"Error fetching subscription tiers for rate card: {e}")