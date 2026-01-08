from app import ma, db
from marshmallow import validates_schema, ValidationError
from models.rate_card import RateCard
from models import Subscription
from uuid import UUID
from datetime import datetime

class RateCardReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RateCard
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)



class RateCardWriteSchema(ma.SQLAlchemySchema):
    subscription_id = ma.auto_field(required=True)
    start_date = ma.auto_field(required=True)
    end_date = ma.auto_field(required=True)
    

    class Meta:
        model = RateCard

    @validates_schema
    def validate_dates(self, data, **kwargs):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError('start_date must be before end_date.')

        subscription_id = data.get('subscription_id')
        if subscription_id:
            subscription = db.session.get(Subscription, UUID(subscription_id))
            if not subscription:
                raise ValidationError('subscription_id does not exist.')

            if start_date and end_date:
                overlapping_rate_cards = RateCard.query.filter(
                    RateCard.subscription_id == subscription_id,
                    RateCard.start_date < end_date,
                    RateCard.end_date > start_date
                ).all()

                if overlapping_rate_cards:
                    raise ValidationError('The provided date range overlaps with an existing rate card for this subscription.')

rate_card_read_schema = RateCardReadSchema()
rate_card_write_schema = RateCardWriteSchema()
rate_cards_read_schema = RateCardReadSchema(many=True)