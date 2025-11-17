from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return "index page"


#################USER ENDPOINTS START#####################
@app.route('/createUser', methods=['POST'])
def createUser():
    '''
    Create a new user and save in DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send user details in JSON format"}, 400
    
    data = request.get_json()

    user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    db.session.add(user)
    db.session.commit()
    return {"message": "User created", "user_id": user.id}, 201

#################USER ENDPOINTS END#####################



#################CONTRACT ENDPOINTS START#####################
@app.route('/createContract', methods=['POST'])
def createContract():
    '''
    Create a new contract and save in DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send contract details in JSON format"}, 400
    
    # Extract data from json request
    data = request.get_json()

    contract = Contract(
        contract_id=data.get('contract_id'),
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

@app.route('/deleteContract', methods=['DELETE'])
def deleteContractByID():
    '''
    Delete existing contract from DB using contract ID
    '''
    pass 

@app.route('/getContract', methods=['GET'])
def getContractByID():
    '''
    Get existing contract from DB using contract ID
    '''
    pass 

def getContractByClient():
    '''
    Get existing contract from DB using Client ID
    '''
    pass
#################CONTRACT ENDPOINTS END#####################

#################DATABASE MODELS START#####################
class User(db.Model):
    """
    Client.who sign contracts for APIs with the company
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# ---

class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    contract_id = db.Column(db.String(50), primary_key=True, unique=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    api_id = db.Column(db.String(100), nullable=False)
    contract_type = db.Column(db.String(50))
    pricing_type = db.Column(db.String(50))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    contract_status = db.Column(db.String(20), default='Draft', nullable=False)
    value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Contract {self.contract_id}>'

class Product(db.Model):
    """
    API products from company
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    version = db.Column(db.String(5), nullable=False)
    pricing_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, default=0.0)
    calls_per_month = db.Column(db.Integer, default=0)
    call_limit_type = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return f'<Product {self.api_id} ({self.name},{self.version})>'

##################DATABASE MODELS END#####################

if __name__ == '__main__':
    app.run(debug=True)