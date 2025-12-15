from app import ma
from models.subscription_tier import Subscription_tier


class SubscriptionTierReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Subscription_tier
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class SubscriptionTierWriteSchema(ma.SQLAlchemySchema):

    subscription_id = ma.auto_field(required=True)
    min_calls = ma.auto_field(required=True)
    max_calls = ma.auto_field(required=True)
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    base_price = ma.auto_field(required=True)
    price_per_tier = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    
    class Meta:
        model = Subscription_tier

subscription_tier_read_schema = SubscriptionTierReadSchema()

subscription_tier_write_schema = SubscriptionTierWriteSchema()

subscription_tiers_read_schema = SubscriptionTierReadSchema(many=True)