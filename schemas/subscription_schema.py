from app import ma, db
from models.subscription import Subscription
from marshmallow import validates_schema, ValidationError, fields
from models import Contract, Product
from uuid import UUID
from datetime import datetime

class SubscriptionReadSchema(ma.SQLAlchemyAutoSchema):

    product = ma.Nested('ProductReadSchema')
    #tiers = ma.Nested('SubscriptionTierReadSchema', many=True)
    tiers = fields.Method("get_active_tiers")

    class Meta:
        model = Subscription
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

    def get_active_tiers(self, obj):
        # Only include tiers that are not archived
        active_tiers = [t for t in obj.tiers if not getattr(t, "is_archived", False)]
        from schemas.subscription_tier_schema import SubscriptionTierReadSchema
        return SubscriptionTierReadSchema(many=True).dump(active_tiers)

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

    @validates_schema
    def validate_pricing_and_strategy(self, data, **kwargs):
        pricing_type = data.get("pricing_type")
        strategy = data.get("strategy")
        if pricing_type == "Fixed":
            if strategy != "Fxed":
                raise ValidationError({"strategy": "Strategy must be 'fixed' when pricing_type is 'Fixed'."})
        elif pricing_type == "Variable":
            if strategy == "fixed":
                raise ValidationError({"strategy": "Strategy cannot be 'fixed' when pricing_type is 'Variable'."})
            if strategy not in ["fill", "pick", "flat"]:
                raise ValidationError({"strategy": "Strategy must be one of 'fill', 'pick', or 'flat' when pricing_type is 'Variable'."})

subscription_read_schema = SubscriptionReadSchema()

subscription_write_schema = SubscriptionWriteSchema()

subscriptions_read_schema = SubscriptionReadSchema(many=True)