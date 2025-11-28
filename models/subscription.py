from app import db
from datetime import datetime
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Subscription(db.Model):
    """
    Subscription types for products
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    contract_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contract.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    pricing_type = db.Column(Enum("Fixed", "Variable", name="pricing_type_enum"),nullable=False) 
    strategy = db.Column(Enum("Pick", "Fill", "Flat", "Fixed", name="strategy_enum"),nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)

    tiers = db.relationship('Subscription_tier', backref='subscription', lazy=True)

    def __repr__(self):
        return f'Subscription_ID: {self.id}, Contract_ID: {self.contract_id}, Product_ID: {self.product_id}'
