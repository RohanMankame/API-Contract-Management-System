from app import ma, db
from models.contract import Contract
from marshmallow import validates_schema, ValidationError
from models import Client
from uuid import UUID
from models.product import Product



class ContractReadSchema(ma.SQLAlchemyAutoSchema):

    subscriptions = ma.Nested('SubscriptionReadSchema', many=True)

    class Meta:
        model = Contract
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class ContractWriteSchema(ma.SQLAlchemySchema):
    
    client_id = ma.auto_field(required=True)
    contract_name = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    
    class Meta:
        model = Contract

    # make sure client_id exists
    @validates_schema
    def check_client_exists(self, data, **kwargs):
        client_id = data.get("client_id")
        if client_id:
            id_obj = UUID(client_id) if isinstance(client_id, str) else client_id
            if not db.session.get(Client, id_obj):
                raise ValidationError({"client_id":"Client does not exist"})
            
    

    

    


contract_read_schema = ContractReadSchema()

contract_write_schema = ContractWriteSchema()

contracts_read_schema = ContractReadSchema(many=True)
