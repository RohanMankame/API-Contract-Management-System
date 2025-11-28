from app import db
from mixins import IdMixin, AuditMixin, BlameMixin

class Subscription(IdMixin, AuditMixin, OperatorMixin, db.Model):
    '''
    Subscription types for products
    '''
    contract_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('contract.id'), nullable=False)
    product_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('product.id'), nullable=False)
    # 1: Fixed, 2: Variable
    pricing_type = db.Column(db.Enum(1, 2, name="pricing_type_enum"),nullable=False) 
    # 1: Pick, 2: Fill, 3: Flat, 4: Fixed
    strategy = db.Column(db.Enum(1, 2, 3, 4, name="strategy_enum"),nullable=False)
    is_archived = db.Column(db.Boolean, default=False)

    tiers = db.relationship('Subscription_tier', backref='subscription', lazy=True)

    def __repr__(self):
        return f'Subscription_ID: {self.id}, Contract_ID: {self.contract_id}, Product_ID: {self.product_id}'

