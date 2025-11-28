from app import db
from datetime import datetime
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
    is_archived = db.Column(db.Boolean, default=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'Company_ID:{self.id}, Company: {self.company_name}, Email: {self.email}'
