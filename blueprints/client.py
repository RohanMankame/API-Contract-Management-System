from flask import Blueprint, request, jsonify
from app import db
from models import Client

client_bp = Blueprint('client', __name__)


@client_bp.route('/createClient', methods=['POST'])
def createClient():
    '''
    Create a new Client and save in DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send user details in JSON format"}, 400
    
    data = request.get_json()
    try:
        client = Client(
            username=data.get('username'),
            email=data.get('email')
        )
        db.session.add(client)
        db.session.commit()
        return {"message": "Client created", "client_id": client.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
        

@client_bp.route('/getClients', methods=['GET'])
def getClients():
    '''
    Get all Clients from DB
    '''
    try:
        clients = Client.query.all()
        clients_list = [{"id": client.id, "username": client.username, "email": client.email} for client in clients]
        return {"client": clients_list}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@client_bp.route('/getClient/<id>', methods=['GET'])
def getClientByID(id):
    '''
    Get existing client from DB using user ID
    '''
    try:
        client = Client.query.get(id)
        if client:
            return {"id": client.id, "username": client.username, "email": client.email}, 200
        else:
            return {"error": "Client not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 400

