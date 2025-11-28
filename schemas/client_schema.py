from app import ma
from models.client import Client

class ClientReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        include_fk = True
        # hide sensitive fields from responses
        exclude = ("created_by", "updated_by",)

class ClientWriteSchema(ma.SQLAlchemySchema):
    
    company_name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone_number = ma.auto_field()
    address = ma.auto_field()
    
    class Meta:
        model = Client
    


client_read_schema = ClientReadSchema()

client_write_schema = ClientWriteSchema()

clients_read_schema = ClientReadSchema(many=True)
