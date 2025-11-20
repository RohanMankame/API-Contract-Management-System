from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Client(db.Model):
    """
    Clients of the company, who purchase API contract
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'




class User(db.Model):
    """
    Employees of business who have access to the system, they can create contracts
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'



class Product(db.Model):
    """
    API products from the company
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    version = db.Column(db.String(5), nullable=False)


    def __repr__(self):
        return f'<Product {self.id} ({self.name},{self.version})>'



class SubscriptionType(db.Model):
    """
    Subscription types for products
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    pricing_type = db.Column(db.String(50), nullable=False)
    price_per_month = db.Column(db.Float, default=0.0)
    calls_per_month = db.Column(db.Integer, default=0)
    call_limit_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<SubscriptionType {self.id} ({self.pricing_type})>'


class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    contract_id = db.Column(db.Integer, primary_key=True, unique=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    contract_type = db.Column(db.String(50))
    product_id = db.Column(db.Integer,db.ForeignKey('product.id') ,nullable=False)
    pricing_type = db.Column(db.String(50))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    contract_status = db.Column(db.String(20), default='Draft', nullable=False)
    value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Contract {self.contract_id}>'

class ContractProduct(db.Model):
    """
    Association table for many-to-many relationship between Contract and Product
    """
    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contract.contract_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('subscription_type.id'), nullable=False)

    contract = db.relationship('Contract', backref=db.backref('contract_products', lazy=True))
    product = db.relationship('Product', backref=db.backref('contract_products', lazy=True))

    def __repr__(self):
        return f'<ContractProduct Contract:{self.contract_id} Product:{self.product_id}>'




