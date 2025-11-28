from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Contract(db.Model):
    """
    Contract between clients and the company.
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'), nullable=False)
    contract_name = db.Column(db.String(100), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    
    subscriptions = db.relationship('Subscription', backref='contract', lazy=True)

    def __repr__(self):
        return f'Contract_ID: {self.id}, contract_name: {self.contract_name}'
