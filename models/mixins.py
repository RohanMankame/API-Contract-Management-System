# models/mixins.py
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app import db

class IdMixin:
    """Add a UUID primary key column"""
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
                   
class AuditMixin:
    """Common audit columns: timestamps and soft-delete flag"""
    is_archived = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class OperatorMixin:
    """Columns referring to the creator/updater user id"""
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)
    updated_by = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)


class DurationMixin:
    """Columns for start and end dates"""
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)