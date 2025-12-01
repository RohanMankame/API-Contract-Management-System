from app import ma
from models.product import Product


class ProductReadSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True
        include_fk = True
        exclude = ("created_by", "updated_by",)

class ProductWriteSchema(ma.SQLAlchemySchema):
    
    product_name = ma.auto_field(required=True)
    description = ma.auto_field()
    is_archived = ma.auto_field()
    
    class Meta:
        model = Product

product_read_schema = ProductReadSchema()

product_write_schema = ProductWriteSchema()

products_read_schema = ProductReadSchema(many=True)