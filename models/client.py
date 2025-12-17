from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin

class Client(IdMixin, AuditMixin, OperatorMixin, db.Model):
    company_name = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    contracts = db.relationship('Contract', backref='client', lazy=True)

    def __repr__(self):
        return f'Company_ID:{self.id}, Company: {self.company_name}, Email: {self.email}'


