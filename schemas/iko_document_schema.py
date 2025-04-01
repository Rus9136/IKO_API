from marshmallow import Schema, fields, validate

class IKODocumentSchema(Schema):
    id = fields.Integer(dump_only=True)
    organization = fields.String(required=True, validate=validate.Length(max=255))
    department = fields.String(required=True, validate=validate.Length(max=255))
    document_number_iko = fields.String(required=True, validate=validate.Length(max=50))
    document_date_iko = fields.Date(required=True)
    warehouse_iko = fields.String(required=True, validate=validate.Length(max=255))
    warehouse_code_iko = fields.String(required=True, validate=validate.Length(max=50))
    operation_iko = fields.String(required=True, validate=validate.Length(max=100))
    product_code_iko = fields.String(required=True, validate=validate.Length(max=50))
    product_name_iko = fields.String(required=True, validate=validate.Length(max=255))
    quantity_iko = fields.Decimal(required=True, places=3)
    price_with_vat_iko = fields.Decimal(required=True, places=2)
    amount_with_vat_iko = fields.Decimal(required=True, places=2)
    vat_amount_iko = fields.Decimal(required=True, places=2)
    vat_rate_iko = fields.Decimal(required=True, places=2)
    cost_price_per_unit_without_vat_iko = fields.Decimal(required=True, places=2)
    cost_price_without_vat_iko = fields.Decimal(required=True, places=2)
    unit_of_measure_iko = fields.String(required=True, validate=validate.Length(max=20))
    shift_number_iko = fields.Integer(required=True)
    cash_register_number_iko = fields.String(required=True, validate=validate.Length(max=50))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

iko_document_schema = IKODocumentSchema()
iko_documents_schema = IKODocumentSchema(many=True)