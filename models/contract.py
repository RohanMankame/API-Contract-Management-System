from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin, DurationMixin
from sqlalchemy.dialects.postgresql import UUID


class Contract(IdMixin, AuditMixin, OperatorMixin, DurationMixin, db.Model,):
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.id'), nullable=False)
    contract_name = db.Column(db.String(100), nullable=False)

    subscriptions = db.relationship('Subscription', backref='contract', lazy=True)

    def __repr__(self):
        return f'Contract_ID: {self.id}, contract_name: {self.contract_name}'

