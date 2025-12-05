from validators import ValidationError
from app import ma, db
from models.user import User
from marshmallow import validates_schema
from marshmallow.validate import Email, Length 



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
    
    class Meta:
        model = User

    @validates_schema
    def validate_unique_email(self, data, **kwargs):
        email = data.get("email")
        if email:
            existing = db.session.query(User).filter_by(email=email).first()
            if existing:
                raise ValidationError({"error": "A user with this email already exists"})

    



user_read_schema = UserReadSchema()

user_write_schema = UserWriteSchema()

users_read_schema = UserReadSchema(many=True)