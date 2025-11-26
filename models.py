from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Client(db.Model):
    """
    Clients of the company, who purchase API contract
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    company_name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    # archived
    is_archived = db.Column(db.Boolean, default=False) 
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'Company_ID:{self.id}, Company: {self.company_name}, Email: {self.email}'



class User(db.Model):
    """
    Employees of business who have access to the system, they can create contracts
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    # archived
    is_archived = db.Column(db.Boolean, default=False) 
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    
    # Password hashing and checking 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    contracts_created = db.relationship('Contract', backref='creator', lazy=True, foreign_keys='Contract.created_by')
    contracts_updated = db.relationship('Contract', backref='updater', lazy=True, foreign_keys='Contract.updated_by')
    
    def __repr__(self):
        return f'User_Id:{self.id}, User: {self.full_name}, Email: {self.email}'



class Product(db.Model):
    """
    API products from the company
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    api_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    
    # archived
    is_archived = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)#added recently
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)#added recently
    
    subscriptions = db.relationship('Subscription', backref='product', lazy=True)

    def __repr__(self):
        return f'Product_Id: {self.id}, API:{self.api_name}'



class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'), nullable=False)
    contract_name = db.Column(db.String(100), nullable=False)

   
    
    # archived
    is_archived = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    
    subscriptions = db.relationship('Subscription', backref='contract', lazy=True)

    def __repr__(self):
        return f'Contract_ID: {self.id}, contract_name: {self.contract_name}'



class Subscription(db.Model):
    """
    Subscription types for products
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    contract_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contract.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    pricing_type = db.Column(Enum("Fixed", "Variable", name="pricing_type_enum"),nullable=False) 
    strategy = db.Column(Enum("Pick", "Fill", "Flat", "Fixed", name="strategy_enum"),nullable=False)
    # archived
    is_archived = db.Column(db.Boolean, default=False)
    # timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)

    tiers = db.relationship('Subscription_tier', backref='subscription', lazy=True)

    def __repr__(self):
        return f'Subscription_ID: {self.id}, Contract_ID: {self.contract_id}, Product_ID: {self.product_id}'




class Subscription_tier(db.Model):
    '''
    tiers for subscriptions
    '''
    id =db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subscription_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subscription.id'), nullable=False)
    min_calls = db.Column(db.Integer, nullable=False)
    max_calls = db.Column(db.Integer, nullable=False)
    
    #just added should change to not nullable later
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    
    base_price = db.Column(db.Float, nullable=True) # For Fixed and Flat strategies
    price_per_tier = db.Column(db.Float, nullable=True) # For Pick and Fill strategies
    # archived
    is_archived = db.Column(db.Boolean, default=False)
    # Users
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)


    def __repr__(self):
        return f'Tier_id: {self.id}, sub_id:{self.subscription_id}, calls:{self.min_calls}-{self.max_calls}'

    