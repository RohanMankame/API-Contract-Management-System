from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Product(db.Model):
    """
    API products from the company
    """
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    api_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    
    subscriptions = db.relationship('Subscription', backref='product', lazy=True)

    def __repr__(self):
        return f'Product_Id: {self.id}, API:{self.api_name}'
