from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime




class Client(db.Model):
    """
    Client.who sign contracts for APIs with the company
    """
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class User(db.Model):
    """
    Employees who input contracts into the system
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

# ---

class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    contract_id = db.Column(db.Integer, primary_key=True, unique=True) 
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    api_id = db.Column(db.Integer,db.ForeignKey('product.id') ,nullable=False)
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
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    version = db.Column(db.String(5), nullable=False)
    pricing_type = db.Column(db.String(50), nullable=False)
    price_per_month = db.Column(db.Float, default=0.0)
    calls_per_month = db.Column(db.Integer, default=0)
    call_limit_type = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return f'<Product {self.api_id} ({self.name},{self.version})>'