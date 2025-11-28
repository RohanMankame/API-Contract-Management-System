from app import db
from models.mixins import IdMixin, AuditMixin, BlameMixin

class Product(IdMixin, AuditMixin, OperatorMixin, db.Model):
    api_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    subscriptions = db.relationship('Subscription', backref='product', lazy=True)

    def __repr__(self):
        return f'Product_Id: {self.id}, API:{self.api_name}'
