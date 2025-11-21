from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
import os
from flask_cors import CORS

# Initialize DB
db = SQLAlchemy()

# Application Factory
def create_app():

    # Flask app setup
    app = Flask(__name__)

    # Load in environment variables and enable CORS
    load_dotenv()
    CORS(app)

    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # JWT Manager setup
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swaggerDoc1.4.json'  
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "API Contract Management System Project"},)
    app.register_blueprint(swaggerui_blueprint)

    # Register Blueprints
    # authentication
    from blueprints.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='')
    # user 
    from blueprints.user import user_bp
    app.register_blueprint(user_bp, url_prefix='')
    # client
    from blueprints.client import client_bp
    app.register_blueprint(client_bp, url_prefix='')
    # product
    from blueprints.product import product_bp
    app.register_blueprint(product_bp, url_prefix='')
    # contract
    from blueprints.contract import contract_bp
    app.register_blueprint(contract_bp, url_prefix='')

    from blueprints.Subscription import Subscription_bp
    app.register_blueprint(Subscription_bp, url_prefix='')

    from blueprints/Subscription_tier import Subscription_tier_bp
    app.register_blueprint(Subscription_tier_bp, url_prefix='')

    # Create database tables if not exist
    with app.app_context():
        db.create_all()
    
    return app

