from app import ma
from models.subscription import Subscription


class SubscriptionReadSchema(ma.SQLAlchemyAutoSchema):
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

subscription_read_schema = SubscriptionReadSchema()

subscription_write_schema = SubscriptionWriteSchema()

subscriptions_read_schema = SubscriptionReadSchema(many=True)