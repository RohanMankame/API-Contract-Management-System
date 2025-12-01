from app import ma
from models.contract import Contract


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

contract_read_schema = ContractReadSchema()

contract_write_schema = ContractWriteSchema()

contracts_read_schema = ContractReadSchema(many=True)
