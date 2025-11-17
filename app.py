from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)


#***********************|DATABASE CONNECTION START|*********************#
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#######################|DATABASE CONNECTION END|##########################



#***********************|SWAGGER DOC START|*********************#

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swaggerDoc.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

app.register_blueprint(swaggerui_blueprint)

#######################|SWAGGER DOC END|##########################

@app.route('/')
def index():
    return "index page"


#***********************|USER/Clients ENDPOINTS START|*********************#
@app.route('/createUser', methods=['POST'])
def createUser():
    '''
    Create a new user and save in DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send user details in JSON format"}, 400
    
    data = request.get_json()
    try:
        user = User(
            username=data.get('username'),
            email=data.get('email')
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created", "user_id": user.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
        

@app.route('/getUsers', methods=['GET'])
def getUsers():
    '''
    Get all users from DB
    '''
    try:
        users = User.query.all()
        users_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
        return {"users": users_list}, 200
    except Exception as e:
        return {"error": str(e)}, 400


@app.route('/getUser', methods=['GET'])
def getUserByID():
    '''
    Get existing user from DB using user ID
    '''
    """ 
    try:
    

    except Exception as e:
        return {"error": str(e)}, 400 
    """



#################|USER/Clients ENDPOINTS END|#####################



#***********************|CONTRACT ENDPOINTS START|*********************#
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

@app.route('/archiveContract', methods=['DELETE'])
def deleteContractByID():
    '''
    Delete existing contract from DB using contract ID
    '''
    pass 

@app.route('/updateContract', methods=['PUT'])
def updateContractByID():
    '''
    Update existing contract in DB using contract ID
    '''
    pass

@app.route('/getContracts', methods=['GET'])
def getAllContracts():
    '''
    Get all existing contracts from DB
    '''
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
#################|CONTRACT ENDPOINTS END|#####################

#***********************|PRODUCTS(APIs) START|*********************#

@app.route('/createProduct', methods=['POST'])
def createProduct():
    '''
    create a new API product and add to DB
    '''
    if not request.is_json:
        return {"error": "Invalid input, send product details in JSON format"}, 400
    data = request.get_json()
    try:
        product = Product(
            name=data.get('name'),
            version=data.get('version'),
            pricing_type=data.get('pricing_type'),
            price=float(data.get('price', 0.0)),
            calls_per_month=int(data.get('calls_per_month', 0)),
            call_limit_type=data.get('call_limit_type')
        )
        db.session.add(product)
        db.session.commit()
        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 400
    




#########################|PRODUCTS(APIs) END|#####################



#***********************|DATABASE MODELS START|*********************#
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

##################|DATABASE MODELS END|#####################



if __name__ == '__main__':
    app.run(debug=True)