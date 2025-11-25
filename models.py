from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Enum

class Client(db.Model):
    """
    Clients of the company, who purchase API contract
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    company_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'<Client {self.company_name}>'



class User(db.Model):
    """
    Employees of business who have access to the system, they can create contracts
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    contracts_created = db.relationship('Contract',foreign_keys='Contract.created_by_user_id',backref='created_by_user',lazy=True)

    contracts_updated = db.relationship('Contract',foreign_keys='Contract.updated_by_user_id',backref='updated_by_user',lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'



class Product(db.Model):
    """
    API products from the company
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    api_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    subscriptions = db.relationship('Subscription',backref='product',lazy=True)

    def __repr__(self):
        return f'<Product {self.id} ({self.api_name})>'



class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    id = db.Column(db.Integer, primary_key=True, unique=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    contract_type = db.Column(db.String(50))
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    updated_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contract_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_archived = db.Column(db.Boolean, default=False)

    subscriptions = db.relationship('Subscription',backref='contract',lazy=True)

    def __repr__(self):
        return f'<Contract {self.id}>'

class Subscription(db.Model):
    """
    Subscription types for products
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    pricing_type = db.Column(Enum("Fixed", "Variable", name="pricing_type_enum"),nullable=False) 
    varible_strategy = db.Column(db.String(100))  
    base_price = db.Column(db.Float, nullable=False)

    tiers = db.relationship('Subscription_tier',backref='subscription',lazy=True)

    def __repr__(self):
        return f'<Subscription {self.id} ({self.contract_id}, {self.product_id})>'


class Subscription_tier(db.Model):
    '''
    for 'pick a tier' and 'fill a tier' tiers
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    tier_name = db.Column(db.String(100), nullable=False)
    min_calls = db.Column(db.Integer, nullable=False)
    max_calls = db.Column(db.Integer, nullable=False)
    price_per_tier = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Tier {self.id} ({self.subscription_id}, {self.tier_name})>'

    