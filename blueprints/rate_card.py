from flask import Blueprint, request
from app import db
from models import rate_card 
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.rate_card_schema import rate_card_read_schema, rate_cards_read_schema, rate_card_write_schema
from marshmallow import ValidationError
from uuid import UUID
from utils.response import ok, created, bad_request, not_found, server_error

rate_card_bp = Blueprint('rate_card', __name__)