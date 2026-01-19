from app import ma, db
from models.contract import Contract
from marshmallow import validates_schema, ValidationError, fields
from models import Client
from uuid import UUID
from models.product import Product



class ContractReadSchema(ma.SQLAlchemyAutoSchema):

    subscriptions = fields.Method("get_active_subscriptions")

    class Meta:
        model = Contract
        load_instance = True
        include_fk = True
        #exclude = ("created_by", "updated_by",)

    def get_active_subscriptions(self, obj):
        # Only include subscriptions that are not archived
        active_subs = [s for s in obj.subscriptions if not getattr(s, "is_archived", False)]
        from schemas.subscription_schema import SubscriptionReadSchema
        return SubscriptionReadSchema(many=True).dump(active_subs)

    




class ContractWriteSchema(ma.SQLAlchemySchema):
    
    client_id = ma.auto_field(required=True)
    contract_name = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    start_date = ma.auto_field(required=True)
    end_date = ma.auto_field(required=True)
    
    class Meta:
        model = Contract

    # make sure client_id exists
    @validates_schema
    def check_client_exists(self, data, **kwargs):
        client_id = data.get("client_id")
        if client_id:
            id_obj = UUID(client_id) if isinstance(client_id, str) else client_id
            if not db.session.get(Client, id_obj):
                raise ValidationError({"error":"Client does not exist"})

    @validates_schema
    def check_end_date_after_start_date(self, data, **kwargs):
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date and end_date <= start_date:
            raise ValidationError({"error": "End date must be after start date"})

            
    

    

    


contract_read_schema = ContractReadSchema()

contract_write_schema = ContractWriteSchema()

contracts_read_schema = ContractReadSchema(many=True)
