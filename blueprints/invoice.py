from flask import Blueprint, request, jsonify, Response
from app import db
from models import Contract
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.serilizer import serialize_contract
import json