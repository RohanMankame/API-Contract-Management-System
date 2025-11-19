from flask import Blueprint, request, jsonify
from app import db
from models import Contract
from datetime import datetime
from flask_jwt_extended import jwt_required

# Initialize contract Blueprint
contract_bp = Blueprint('contract', __name__)

# Contract Endpoints

@contract_bp.route('/Contracts', methods=['POST','GET'])
@jwt_required()
def Contracts():
    '''
    Post: Create a new contract
    Get: Get all contracts from DB
    '''
    # Create new contract
    if methods == 'POST':
        if not request.is_json:
            return {"error": "Invalid input, send contract details in JSON format"}, 400
        
        data = request.get_json()

        try:
            contract = Contract(
                #contract_id=data.get('contract_id'),
                client_id=data.get('client_id'),
                api_id=data.get('api_id'),
                contract_type=data.get('contract_type'),
                pricing_type=data.get('pricing_type'),
                start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d'),
                end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d'),
                contract_status=data.get('contract_status', 'Draft'),
                value=float(data.get('value', 0.0))
            )
            db.session.add(contract)
            db.session.commit()
            return {"message": "Contract created", "contract_id": contract.contract_id}, 201 

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400 


    # Get all contracts
    elif methods == 'GET':
        try:
            contracts = Contract.query.all()
            contracts_list = [{
                "contract_id": contract.contract_id,
                "client_id": contract.client_id,
                "api_id": contract.api_id,
                "contract_type": contract.contract_type,
                "pricing_type": contract.pricing_type,
                "start_date": contract.start_date.strftime('%Y-%m-%d'),
                "end_date": contract.end_date.strftime('%Y-%m-%d'),
                "contract_status": contract.contract_status,
                "value": contract.value
            } for contract in contracts]
            
            return {"contracts": contracts_list}, 200

        except Exception as e:
            return {"error": str(e)}, 400



@contract_bp.route('/Contracts/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def Contract_id(id):
    '''
    GET: Get existing contract from DB using contract ID
    PUT: Update existing contract in DB using contract ID
    DELETE: Delete existing contract from DB using contract ID
    '''
    # Get existing contract from DB using contract ID
    if methods == 'GET':
        try:
            contract = Contract.query.get(contractID)
            if contract:
                return {
                    "contract_id": contract.contract_id,
                    "client_id": contract.client_id,
                    "api_id": contract.api_id,
                    "contract_type": contract.contract_type,
                    "pricing_type": contract.pricing_type,
                    "start_date": contract.start_date.strftime('%Y-%m-%d'),
                    "end_date": contract.end_date.strftime('%Y-%m-%d'),
                    "contract_status": contract.contract_status,
                    "value": contract.value
                }, 200
            else:
                return {"error": "Contract not found"}, 404
                
        except Exception as e:
            return {"error": str(e)}, 400

    # Update existing contract in DB using contract ID
    elif methods == 'PUT':
        if not request.is_json:
            return {"error": "Invalid input, send contract details in JSON format"}, 400

        data = request.get_json()
        
        try:
            contract = Contract.query.get(contractID)

            if not contract:
                return {"error": "Contract not found"}, 404

            contract.client_id = data.get('client_id', contract.client_id)
            contract.api_id = data.get('api_id', contract.api_id)
            contract.contract_type = data.get('contract_type', contract.contract_type)
            contract.pricing_type = data.get('pricing_type', contract.pricing_type)
            contract.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d') if data.get('start_date') else contract.start_date
            contract.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if data.get('end_date') else contract.end_date
            contract.contract_status = data.get('contract_status', contract.contract_status)
            contract.value = float(data.get('value', contract.value))

            db.session.commit()
            return {"message": "Contract updated", "contract_id": contract.contract_id}, 200

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


    # Delete existing contract from DB using contract ID
    elif methods == 'DELETE':
        try:
            contract = Contract.query.get(contractID)
            if not contract:
                return {"error": "Contract not found, no contract was deleted"}, 404
            
            db.session.delete(contract)
            db.session.commit()
            return {"message": f"Contract with id:{contractID} has been deleted"}, 200
            
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400


@contract_bp.route('/Contracts/<id>/Product', methods=['POST','GET', 'PUT', 'DELETE'])
@jwt_required()
def Contract_Product_id(id):
    if methods == 'GET':
        try:
            contracts = Contract.query.filter_by(api_id=id).all()
            contracts_list = [{
                "contract_id": contract.contract_id,
                "client_id": contract.client_id,
                "api_id": contract.api_id,
                "contract_type": contract.contract_type,
                "pricing_type": contract.pricing_type,
                "start_date": contract.start_date.strftime('%Y-%m-%d'),
                "end_date": contract.end_date.strftime('%Y-%m-%d'),
                "contract_status": contract.contract_status,
                "value": contract.value
            } for contract in contracts]
            return {"contracts": contracts_list}, 200

        except Exception as e:
            return {"error": str(e)}, 400

    elif methods == 'POST':

    elif methods == 'DELETE':

    elif methods == 'PUT':


@contract_bp.route('/Contracts/<id>/Client', methods=['POST','GET', 'PUT', 'DELETE'])
@jwt_required()
def Contract_Product_id(id):
    if methods == 'GET':

    elif methods == 'POST':

    elif methods == 'DELETE':

    elif methods == 'PUT':























'''
@contract_bp.route('/createContract', methods=['POST'])
@jwt_required()
def createContract():
    
    if not request.is_json:
        return {"error": "Invalid input, send contract details in JSON format"}, 400
    
    data = request.get_json()
    try:
        contract = Contract(
            #contract_id=data.get('contract_id'),
            client_id=data.get('client_id'),
            api_id=data.get('api_id'),
            contract_type=data.get('contract_type'),
            pricing_type=data.get('pricing_type'),
            start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d'),
            end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d'),
            contract_status=data.get('contract_status', 'Draft'),
            value=float(data.get('value', 0.0))
        )
        db.session.add(contract)
        db.session.commit()
        return {"message": "Contract created", "contract_id": contract.contract_id}, 201 

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400 



    

@contract_bp.route('/getContracts', methods=['GET'])
@jwt_required()
def getContracts():
    
    try:
        contracts = Contract.query.all()
        contracts_list = [{
            "contract_id": contract.contract_id,
            "client_id": contract.client_id,
            "api_id": contract.api_id,
            "contract_type": contract.contract_type,
            "pricing_type": contract.pricing_type,
            "start_date": contract.start_date.strftime('%Y-%m-%d'),
            "end_date": contract.end_date.strftime('%Y-%m-%d'),
            "contract_status": contract.contract_status,
            "value": contract.value
        } for contract in contracts]
        return {"contracts": contracts_list}, 200

    except Exception as e:
        return {"error": str(e)}, 400





@contract_bp.route('/getContract/<contractID>', methods=['GET'])
@jwt_required()
def getContractByID(contractID):
    '''
    #Get existing contract from DB using contract ID
    '''
    try:
        contract = Contract.query.get(contractID)
        if contract:
            return {
                "contract_id": contract.contract_id,
                "client_id": contract.client_id,
                "api_id": contract.api_id,
                "contract_type": contract.contract_type,
                "pricing_type": contract.pricing_type,
                "start_date": contract.start_date.strftime('%Y-%m-%d'),
                "end_date": contract.end_date.strftime('%Y-%m-%d'),
                "contract_status": contract.contract_status,
                "value": contract.value
            }, 200
        else:
            return {"error": "Contract not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 400
     



@contract_bp.route('/getContractsByUser/<userID>', methods=['GET'])
@jwt_required()
def getContractByUserID(userID):
    '''
    #Get existing contract from DB using Client ID
    '''
    try:
        contracts = Contract.query.filter_by(client_id=userID).all()
        contracts_list = [{
            "contract_id": contract.contract_id,
            "client_id": contract.client_id,
            "api_id": contract.api_id,
            "contract_type": contract.contract_type,
            "pricing_type": contract.pricing_type,
            "start_date": contract.start_date.strftime('%Y-%m-%d'),
            "end_date": contract.end_date.strftime('%Y-%m-%d'),
            "contract_status": contract.contract_status,
            "value": contract.value
        } for contract in contracts]
        return {"contracts": contracts_list}, 200

    except Exception as e:
        return {"error": str(e)}, 400






@contract_bp.route('/getContractsByProduct/<productID>', methods=['GET'])
@jwt_required()
def getContractsByProductID(productID):
    '''
    #Get existing contract from DB using Client ID
    '''
    try:
        contracts = Contract.query.filter_by(api_id=productID).all()
        contracts_list = [{
            "contract_id": contract.contract_id,
            "client_id": contract.client_id,
            "api_id": contract.api_id,
            "contract_type": contract.contract_type,
            "pricing_type": contract.pricing_type,
            "start_date": contract.start_date.strftime('%Y-%m-%d'),
            "end_date": contract.end_date.strftime('%Y-%m-%d'),
            "contract_status": contract.contract_status,
            "value": contract.value
        } for contract in contracts]
        return {"contracts": contracts_list}, 200

    except Exception as e:
        return {"error": str(e)}, 400






@contract_bp.route('/updateContract/<contractID>', methods=['PUT'])
@jwt_required()
def updateContractByID(contractID):
    '''
    #Update existing contract in DB using contract ID
    '''
    if not request.is_json:
            return {"error": "Invalid input, send contract details in JSON format"}, 400

    data = request.get_json()
    
    try:
        contract = Contract.query.get(contractID)

        if not contract:
            return {"error": "Contract not found"}, 404

        contract.client_id = data.get('client_id', contract.client_id)
        contract.api_id = data.get('api_id', contract.api_id)
        contract.contract_type = data.get('contract_type', contract.contract_type)
        contract.pricing_type = data.get('pricing_type', contract.pricing_type)
        contract.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d') if data.get('start_date') else contract.start_date
        contract.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d') if data.get('end_date') else contract.end_date
        contract.contract_status = data.get('contract_status', contract.contract_status)
        contract.value = float(data.get('value', contract.value))

        db.session.commit()
        return {"message": "Contract updated", "contract_id": contract.contract_id}, 200

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400






@contract_bp.route('/deleteContract/<contractID>', methods=['DELETE'])
@jwt_required()
def deleteContractByID(contractID):
    '''
    #Delete existing contract from DB using contract ID
    '''
    try:
        contract = Contract.query.get(contractID)
        if not contract:
            return {"error": "Contract not found, no contract was deleted"}, 404
        
        db.session.delete(contract)
        db.session.commit()
        return {"message": f"Contract with id:{contractID} has been deleted"}, 200
        
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
    
      