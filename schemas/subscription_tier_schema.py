from app import ma, db
from models.subscription_tier import SubscriptionTier 
from marshmallow import validates_schema, ValidationError
from models import RateCard
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
            try:
                id_obj = UUID(rate_card_id) if isinstance(rate_card_id, str) else rate_card_id
            except Exception:
                raise ValidationError({"rate_card_id": "Invalid UUID format"})
            if not db.session.get(RateCard, id_obj):
                raise ValidationError({"rate_card_id": "RateCard does not exist"})


subscription_tier_read_schema = SubscriptionTierReadSchema()

subscription_tier_write_schema = SubscriptionTierWriteSchema()

subscription_tiers_read_schema = SubscriptionTierReadSchema(many=True)