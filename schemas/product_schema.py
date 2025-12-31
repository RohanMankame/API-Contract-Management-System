from app import ma
from models.product import Product

from marshmallow import validates_schema, ValidationError


class ProductReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class ProductWriteSchema(ma.SQLAlchemySchema):
    
    api_name = ma.auto_field(required=True)
    description = ma.auto_field()
    is_archived = ma.auto_field()
    
    class Meta:
        model = Product

    @validates_schema
    def validate_api_name(self, data, **kwargs):
        api_name = data.get("api_name")
        if api_name == "TestFailProduct":
            raise ValidationError({"error": "API name cannot be 'TestFailProduct'"})


product_read_schema = ProductReadSchema()

product_write_schema = ProductWriteSchema()

products_read_schema = ProductReadSchema(many=True)