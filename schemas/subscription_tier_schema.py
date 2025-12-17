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

    subscription_id = ma.auto_field(required=True)
    min_calls = ma.auto_field(required=True)
    max_calls = ma.auto_field(required=True)
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    base_price = ma.auto_field(required=True)
    price_per_tier = ma.auto_field(required=True)
    is_archived = ma.auto_field()
    
    class Meta:
        model = SubscriptionTier 

    @validates_schema
    def validate_dependency(self, data, **kwargs):
        # check min/max
        if "min_calls" in data and "max_calls" in data and data["min_calls"] > data["max_calls"]:
            raise ValidationError({"min_calls": "min_calls must be <= max_calls"})
        # check subscription exists
        subscription_id = data.get("subscription_id")
        if subscription_id:
            try:
                id_obj = UUID(subscription_id) if isinstance(subscription_id, str) else subscription_id
            except Exception:
                raise ValidationError({"error": "Invalid UUID format"})
            if not db.session.get(Subscription, id_obj):
                raise ValidationError({"error": "Subscription does not exist"})

    @validates_schema
    def validate_dates(self, data, **kwargs):
        s = data.get("start_date")
        e = data.get("end_date")
        if s is not None and e is not None:
            
            if isinstance(s, str):
                try:
                    s = datetime.fromisoformat(s)
                except Exception:
                    raise ValidationError({"error": "Invalid start_date format; expected ISO-8601."})
            if isinstance(e, str):
                try:
                    e = datetime.fromisoformat(e)
                except Exception:
                    raise ValidationError({"error": "Invalid end_date format; expected ISO-8601."})
            if s >= e:
                raise ValidationError({"error": "start_date must be before end_date."})





subscription_tier_read_schema = SubscriptionTierReadSchema()

subscription_tier_write_schema = SubscriptionTierWriteSchema()

subscription_tiers_read_schema = SubscriptionTierReadSchema(many=True)