from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin, DurationMixin
from sqlalchemy.dialects.postgresql import UUID

class Subscription_tier(IdMixin, AuditMixin, OperatorMixin, DurationMixin, db.Model):
    '''
    tiers for subscriptions
    '''
    subscription_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('subscription.id'), nullable=False)
    min_calls = db.Column(db.Integer, nullable=False)
    max_calls = db.Column(db.Integer, nullable=False)
    base_price = db.Column(db.Float, nullable=True) # For Fixed and Flat strategies
    price_per_tier = db.Column(db.Float, nullable=True) # For Pick and Fill strategies

    def __repr__(self):
        return f'Tier_id: {self.id}, sub_id:{self.subscription_id}, calls:{self.min_calls}-{self.max_calls}'

