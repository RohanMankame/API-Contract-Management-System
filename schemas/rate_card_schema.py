from app import ma, db
from marshmallow import validates_schema, ValidationError, fields
from models.rate_card import RateCard
from models import Subscription, Contract
from models import Subscription
from uuid import UUID
from datetime import datetime, timezone

class RateCardReadSchema(ma.SQLAlchemyAutoSchema):
    tiers = fields.Method("get_active_tiers")
    
    class Meta:
        model = RateCard
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

    def get_active_tiers(self, obj):
        # Only include tiers that are not archived
        active_tiers = [t for t in obj.tiers if not getattr(t, "is_archived", False)]
        from schemas.subscription_tier_schema import SubscriptionTierReadSchema
        return SubscriptionTierReadSchema(many=True).dump(active_tiers)



class RateCardWriteSchema(ma.SQLAlchemySchema):
    subscription_id = ma.auto_field(required=True)
    start_date = ma.auto_field(required=True)
    end_date = ma.auto_field(required=True)
    

    class Meta:
        model = RateCard



    @validates_schema
    def validate_dates(self, data, **kwargs):
        def _to_utc_aware(dt):
            if dt is None:
                return None
            if dt.tzinfo is None:
                return dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc)

        start_date = _to_utc_aware(data.get('start_date'))
        end_date = _to_utc_aware(data.get('end_date'))

        if start_date and end_date and start_date >= end_date:
            raise ValidationError({"error": "The start date must be before the end date. Please correct the dates."})

        subscription_id = data.get('subscription_id')
        if subscription_id:
            subscription = db.session.get(Subscription, subscription_id)
            if not subscription:
                raise ValidationError({"error": "subscription_id does not exist."})

            contract = db.session.get(Contract, subscription.contract_id)
            if not contract:
                raise ValidationError({"error": "Parent contract not found for subscription."})

            contract_start = _to_utc_aware(contract.start_date)
            contract_end = _to_utc_aware(contract.end_date)

            if start_date and contract_start and start_date < contract_start:
                raise ValidationError({"error": "Rate card start_date cannot be before the contract start_date."})

            if end_date and contract_end and end_date > contract_end:
                raise ValidationError({"error": "Rate card end_date cannot be after the contract end_date."})

            current_id = self.context.get("current_rate_card_id")
            # Changed syntax !!!
            query = query = db.session.query(RateCard).filter(
                RateCard.subscription_id == subscription_id,
                RateCard.is_archived == False,
                RateCard.start_date < end_date,
                RateCard.end_date > start_date
            )
            if current_id:
                try:
                    current_uuid = UUID(current_id) if isinstance(current_id, str) else current_id
                    query = query.filter(RateCard.id != current_uuid)
                except Exception:
                    pass

            overlapping_rate_cards = query.all()

            if overlapping_rate_cards:
                raise ValidationError({"error": "The provided date range overlaps with an existing rate card for this subscription. Please choose a different date range."})



rate_card_read_schema = RateCardReadSchema()
rate_card_write_schema = RateCardWriteSchema()
rate_cards_read_schema = RateCardReadSchema(many=True)