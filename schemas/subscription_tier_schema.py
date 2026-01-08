from app import ma, db
from models.subscription_tier import SubscriptionTier 
from marshmallow import validates_schema, ValidationError
from models import Subscription
from uuid import UUID
from datetime import datetime


class SubscriptionTierReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SubscriptionTier 
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class SubscriptionTierWriteSchema(ma.SQLAlchemySchema):

    rate_card_id = ma.auto_field(required=True)
    min_calls = ma.auto_field(required=True)
    max_calls = ma.auto_field(required=True)
    unit_price = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    
    class Meta:
        model = SubscriptionTier 

    @validates_schema
    def validate_dependency(self, data, **kwargs):
        rate_card_id = data.get('rate_card_id')
        if rate_card_id:
            rate_card = db.session.get(Subscription, UUID(rate_card_id))
            if not rate_card:
                raise ValidationError('rate_card_id does not exist.')
       


subscription_tier_read_schema = SubscriptionTierReadSchema()

subscription_tier_write_schema = SubscriptionTierWriteSchema()

subscription_tiers_read_schema = SubscriptionTierReadSchema(many=True)