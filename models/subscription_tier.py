from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin, DurationMixin
from sqlalchemy.dialects.postgresql import UUID

class SubscriptionTier(IdMixin, AuditMixin, OperatorMixin, DurationMixin, db.Model):
    '''
    tiers for subscriptions
    '''
    __tablename__ = "subscription_tier"
    rate_card_id = db.Column(UUID(as_uuid=True), db.ForeignKey('rate_card.id'), nullable=False)
    min_calls = db.Column(db.Integer, nullable=False)
    max_calls = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)

    rate_card = db.relationship('RateCard', back_populates='tiers', lazy=True)


    def __repr__(self):
        return f'Tier_id: {self.id}, sub_id:{self.subscription_id}, calls:{self.min_calls}-{self.max_calls}'

