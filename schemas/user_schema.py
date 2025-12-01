from app import ma
from models.user import User


class UserReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_fk = True
        exclude = ("password_hash", "created_by", "updated_by",)

class UserWriteSchema(ma.SQLAlchemySchema):
    
    email = ma.auto_field(required=True)
    password = ma.String(required=True, load_only=True)
    full_name = ma.auto_field(required=True)
    
    class Meta:
        model = User



user_read_schema = UserReadSchema()

user_write_schema = UserWriteSchema()

users_read_schema = UserReadSchema(many=True)