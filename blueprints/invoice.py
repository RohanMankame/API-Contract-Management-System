from flask import Blueprint, request, jsonify, Response
from app import db
from models import Contract
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.serilizer import serialize_contract
import json


# Initialize contract Blueprint
contract_bp = Blueprint('invoice', __name__)


@contract_bp.route('/invoice', methods=['POST', 'GET'])
@jwt_required()
def invoice():
    if request.method == 'POST':
        try:
            data = request.get_json()

            contract_id = data['contract_id']

            new_invoice = Invoice(
                contract_id = contract_id,
                total_amount = data['total_amount'],
                start_date = data['start_date'],
                end_date = data['end_date'],
                is_archived = data.get('is_archived', False),
                created_by = get_jwt_identity(),
                updated_by = get_jwt_identity()

            )

            db.session.add(new_invoice)
            db.session.commit()
            return jsonify({'message': 'Invoice created successfully', 'invoice_id': new_invoice.id}), 201
        except Exception as e:
            return jsonify({'message': 'Error creating invoice', 'error': str(e)}), 500


    elif request.method == 'GET':
        try:
            invoices = Invoice.query.all()
            invoices_list = []

            for invoice in invoices:
                invoices_list.append({
                    'id': invoice.id,
                    'contract_id': invoice.contract_id,
                    'total_amount': invoice.total_amount,
                    'start_date': invoice.start_date,
                    'end_date': invoice.end_date,
                    'is_archived': invoice.is_archived,
                    'created_at': invoice.created_at,
                    'updated_at': invoice.updated_at,
                    'created_by': invoice.created_by,
                    'updated_by': invoice.updated_by
                })

            return jsonify(invoices_list), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching invoices', 'error': str(e)}), 500
        
    return jsonify({'message': 'Invalid request method'}), 400



@contract_bp.route('/invoice/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def get_invoice(id):

    if request.method == 'GET':
        try:
            invoice = Invoice.query.filter_by(id=id).first()
            if not invoice:
                return jsonify({'message': 'Invoice not found'}), 404

            invoice_data = {
                'id': invoice.id,
                'contract_id': invoice.contract_id,
                'total_amount': invoice.total_amount,
                'start_date': invoice.start_date,
                'end_date': invoice.end_date,
                'is_archived': invoice.is_archived,
                'created_at': invoice.created_at,
                'updated_at': invoice.updated_at,
                'created_by': invoice.created_by,
                'updated_by': invoice.updated_by
            }

            return jsonify(invoice_data), 200

        except Exception as e:
            return jsonify({'message': 'Error fetching invoice', 'error': str(e)}), 500
    
    elif request.method == 'PUT':
        try:
            data = request.get_json()
            invoice = Invoice.query.filter_by(id=id).first()

            if not invoice:
                return jsonify({'message': 'Invoice not found'}), 404

            invoice.contract_id = data.get('contract_id', invoice.contract_id)
            invoice.total_amount = data.get('total_amount', invoice.total_amount)
            invoice.start_date = data.get('start_date', invoice.start_date)
            invoice.end_date = data.get('end_date', invoice.end_date)
            invoice.is_archived = data.get('is_archived', invoice.is_archived)
            invoice.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Invoice updated successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error updating invoice', 'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        try:
            invoice = Invoice.query.filter_by(id=id).first()

            if not invoice:
                return jsonify({'message': 'Invoice not found'}), 404

            invoice.is_archived = True
            invoice.updated_by = get_jwt_identity()

            db.session.commit()
            return jsonify({'message': 'Invoice archived successfully'}), 200

        except Exception as e:
            return jsonify({'message': 'Error deleting invoice', 'error': str(e)}), 500
    
    return jsonify({'message': 'Invalid request method'}), 400
        