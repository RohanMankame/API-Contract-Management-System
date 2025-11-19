from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager



db = SQLAlchemy()

# Application Factory
def create_app():

    # Flask app setup
    app = Flask(__name__)
    load_dotenv()
    # Database setup
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # JWT Manager setup
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    jwt = JWTManager(app)

    # Swagger UI setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swaggerDoc1.3.json'  
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Test application"},)
    app.register_blueprint(swaggerui_blueprint)

    # Register Blueprints
    from blueprints.product import product_bp
    app.register_blueprint(product_bp, url_prefix='')

    from blueprints.client import client_bp
    app.register_blueprint(client_bp, url_prefix='')

    # Create database tables if not exist
    with app.app_context():
        db.create_all()
    
    return app




'''

@app.route('/')
def Home():
    return "Home page"

'''