from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Subscription_tier(db.Model):
    '''
    tiers for subscriptions
    '''
    id =db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    subscription_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subscription.id'), nullable=False)
    min_calls = db.Column(db.Integer, nullable=False)
    max_calls = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    base_price = db.Column(db.Float, nullable=True) # For Fixed and Flat strategies
    price_per_tier = db.Column(db.Float, nullable=True) # For Pick and Fill strategies
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return f'Tier_id: {self.id}, sub_id:{self.subscription_id}, calls:{self.min_calls}-{self.max_calls}'

    