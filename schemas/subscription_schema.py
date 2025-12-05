from app import ma, db
from models.subscription import Subscription
from marshmallow import validates_schema, ValidationError
from models import Contract, Product
from uuid import UUID
from datetime import datetime

class SubscriptionReadSchema(ma.SQLAlchemyAutoSchema):

    product = ma.Nested('ProductReadSchema')
    tiers = ma.Nested('SubscriptionTierReadSchema', many=True)

    class Meta:
        model = Subscription
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class SubscriptionWriteSchema(ma.SQLAlchemySchema):
    
    contract_id = ma.auto_field(required=True)
    product_id = ma.auto_field(required=True)
    pricing_type = ma.auto_field(required=True)
    strategy = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    
    class Meta:
        model = Subscription

    
    @validates_schema
    def validate_parents(self, data, **kwargs):
        # Check contract exists
        contract_id = data.get("contract_id")
        product_id = data.get("product_id")
        if contract_id:
            try:
                id_obj_cont = UUID(contract_id) if isinstance(contract_id, str) else contract_id
            except Exception:
                raise ValidationError({"error": "Invalid UUID format"})
            if not db.session.get(Contract, id_obj_cont):
                raise ValidationError({"error": "Contract does not exist"})
        
        if product_id:
            try:
                id_obj_prod = UUID(product_id) if isinstance(product_id, str) else product_id
            except Exception:
                raise ValidationError({"error": "Invalid UUID format"})
            if not db.session.get(Product, id_obj_prod):
                raise ValidationError({"error": "Product does not exist"})

    

subscription_read_schema = SubscriptionReadSchema()

subscription_write_schema = SubscriptionWriteSchema()

subscriptions_read_schema = SubscriptionReadSchema(many=True)