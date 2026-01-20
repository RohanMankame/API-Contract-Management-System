
from app import ma
from models.client import Client
from marshmallow.validate import Email, Length 

from marshmallow import validates_schema, ValidationError


class ClientReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        include_fk = True
        #exclude = ("created_by", "updated_by",)

class ClientWriteSchema(ma.SQLAlchemySchema):
    
    company_name = ma.auto_field(required=True)
    email = ma.auto_field(required=True, validate=Email(error="Invalid email address"))
    phone_number = ma.auto_field()
    address = ma.auto_field()
    
    class Meta:
        model = Client

    # For test purpose only
    @validates_schema
    def validate_company_name(self, data, **kwargs):
        company_name = data.get("company_name")
        if company_name == "TestFailClient":
            raise ValidationError({"error": "Company name cannot be 'TestFailClient'"})

    
    


client_read_schema = ClientReadSchema()

client_write_schema = ClientWriteSchema()

clients_read_schema = ClientReadSchema(many=True)
