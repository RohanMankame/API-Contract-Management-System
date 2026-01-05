from marshmallow import ValidationError
from app import ma, db
from models.user import User
from marshmallow import validates_schema
from marshmallow.validate import Email, Length, OneOf



class UserReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("password_hash", "created_by", "updated_by",)

class UserWriteSchema(ma.SQLAlchemySchema):
    
    
    email = ma.auto_field(required=True, validate=Email(error="Invalid email address"))
    
    password = ma.String(required=True, load_only=True, validate=Length(min=8, error="Password must be at least 8 characters long"))
    full_name = ma.auto_field(required=True)
    role = ma.String(required=True, validate=OneOf(['employee', 'admin'], error="Role must be 'employee' or 'admin'"))
    
    class Meta:
        model = User

    @validates_schema
    def validate_unique_email(self, data, **kwargs):
        email = data.get("email")
        if email:
            user_id = getattr(self, 'context', {}).get("user_id")
            existing = db.session.query(User).filter_by(email=email).first()
            if existing and (not user_id or str(existing.id) != str(user_id)):
                raise ValidationError({"error": "A user with this email already exists"})

    



user_read_schema = UserReadSchema()

user_write_schema = UserWriteSchema()

users_read_schema = UserReadSchema(many=True)