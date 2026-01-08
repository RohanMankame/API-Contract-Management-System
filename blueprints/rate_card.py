from flask import Blueprint, request
from app import db
from models import rate_card 
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.rate_card_schema import rate_card_read_schema, rate_cards_read_schema, rate_card_write_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

rate_card_bp = Blueprint('rate_card', __name__)

@rate_card_bp.route('/rate-cards', methods=['POST', 'GET'])
@jwt_required()
def Rate_card():
    current_user_id = get_jwt_identity()

    if request.method == 'POST':
        try:
            data = request.get_json()
            validated = rate_card_write_schema.load(data)

            new_rate_card = rate_card(**validated, created_by=current_user_id, updated_by=current_user_id)

            db.session.add(new_rate_card)
            db.session.commit()

            return created(data={"rate_card": rate_card_read_schema.dump(new_rate_card)}, message="Rate card created successfully")
        except ValidationError as ve:
            return bad_request(message="Validation Error", errors=ve.messages)

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error creating rate card: {e}")
    
    elif request.method == 'GET':
        try:
            rate_cards = db.session.query(rate_card).filter_by(is_archived=False).all()
            
            return ok(data={"rate_cards": rate_cards_read_schema.dump(rate_cards)}, message="Rate cards retrieved successfully")

        except Exception as e:
            db.session.rollback()
            return server_error(message=f"Error fetching rate cards: {e}")