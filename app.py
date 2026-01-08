from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

# Initialize DB and Marshmallow
db = SQLAlchemy()
ma = Marshmallow()

# Application Factory
def create_app():

    # Flask app setup
    app = Flask(__name__)

    # Load in environment variables and enable CORS
    load_dotenv()
    CORS(app)

    database_url = os.environ.get('DATABASE_URL')
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY')


    # Database and Marshmallow initialization
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    # JWT Manager setup
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    jwt = JWTManager(app)

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swaggerDoc1.6.json'  
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API Contract Management System Project"},)
    app.register_blueprint(swaggerui_blueprint)




    # Register Blueprints
    # authentication
    from blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    # user 
    from blueprints.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/')
    # client
    from blueprints.client import client_bp
    app.register_blueprint(client_bp, url_prefix='/')
    # product
    from blueprints.product import product_bp
    app.register_blueprint(product_bp, url_prefix='/')
    # contract
    from blueprints.contract import contract_bp
    app.register_blueprint(contract_bp, url_prefix='/')
    # subscription
    from blueprints.subscription import subscription_bp
    app.register_blueprint(subscription_bp, url_prefix='/')

    # rate_card
    from blueprints.rate_card import rate_card_bp
    app.register_blueprint(rate_card_bp, url_prefix='/')

    # subscription_tier
    from blueprints.subscription_tier import subscription_tier_bp
    app.register_blueprint(subscription_tier_bp, url_prefix='/')

    

    # Create database tables if not exist
    with app.app_context():

        
        db.drop_all()
        db.create_all()
    
    return app
