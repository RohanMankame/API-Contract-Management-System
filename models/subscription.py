from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin
from sqlalchemy.dialects.postgresql import UUID

class Subscription(IdMixin, AuditMixin, OperatorMixin, db.Model):
    '''
    Subscription types for products
    '''
    contract_id = db.Column(UUID(as_uuid=True), db.ForeignKey('contract.id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    
    pricing_type = db.Column(db.Enum("Fixed", "Variable", name="pricing_type_enum"),nullable=False) 
    
    strategy = db.Column(db.Enum("Pick", "Fill", "Flat", "Fixed", name="strategy_enum"),nullable=False)
    is_archived = db.Column(db.Boolean, default=False)

    tiers = db.relationship('SubscriptionTier', backref='subscription', lazy=True)

    def __repr__(self):
        return f'Subscription_ID: {self.id}, Contract_ID: {self.contract_id}, Product_ID: {self.product_id}'

