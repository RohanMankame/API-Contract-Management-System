from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin, DurationMixin
from sqlalchemy.dialects.postgresql import UUID
import uuid

class RateCard(IdMixin, AuditMixin, OperatorMixin, DurationMixin, db.Model):
    __tablename__ = 'rate_card'

    subscription_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subscription.id'), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    version = db.Column(db.String(64), nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    subscription = db.relationship('Subscription', back_populates='rate_cards', lazy=True)
    tiers = db.relationship('SubscriptionTier', back_populates='rate_card', cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return f'RateCard:{self.id} subscription:{self.subscription_id} {self.start_date.isoformat()} - {self.end_date.isoformat()}'