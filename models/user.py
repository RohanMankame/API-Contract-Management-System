from app import db
from models.mixins import IdMixin, AuditMixin, OperatorMixin
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

class User(IdMixin, AuditMixin, OperatorMixin, db.Model):
    '''
    Employees of business who have access to the system, they can create contracts
    '''
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    # override mixin fields to be nullable for bootstrapping first user
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    contracts_created = db.relationship('Contract', backref='creator', lazy=True, foreign_keys='Contract.created_by')
    contracts_updated = db.relationship('Contract', backref='updater', lazy=True, foreign_keys='Contract.updated_by')
    
    def __repr__(self):
        return f'User_Id:{self.id}, User: {self.full_name}, Email: {self.email}'


"""
class User(db.Model):

    Employees of business who have access to the system, they can create contracts
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_archived = db.Column(db.Boolean, default=False) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True) # Only for first user creation
    updated_by=db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=True) # Only for first user creation
    
    # Password hashing and checking 
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    contracts_created = db.relationship('Contract', backref='creator', lazy=True, foreign_keys='Contract.created_by')
    contracts_updated = db.relationship('Contract', backref='updater', lazy=True, foreign_keys='Contract.updated_by')
    
    def __repr__(self):
        return f'User_Id:{self.id}, User: {self.full_name}, Email: {self.email}'
"""