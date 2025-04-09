from marshmallow import Schema, fields, validate
from datetime import datetime

class IKOCheckSchema(Schema):
    id = fields.Integer(dump_only=True)
    
    # Информация о кассе и подразделении
    cash_register_name = fields.String(required=True)
    cash_register_serial_number = fields.String(required=True)
    cash_register_number = fields.Integer(required=True)
    department_name = fields.String(required=True)
    department_id = fields.String(required=True)  # UUID как строка
    store_name = fields.String(required=True)
    
    # Информация о чеке
    fiscal_cheque_number = fields.String(required=True)
    order_number = fields.Integer(required=True)
    close_time = fields.DateTime(required=True)
    precheque_time = fields.DateTime(allow_none=True)
    order_type = fields.String(allow_none=True)
    pay_types = fields.String(required=True)
    deleted_with_writeoff = fields.String(allow_none=True)
    
    # Информация о товаре/блюде
    dish_code = fields.String(required=True)
    dish_name = fields.String(required=True)
    dish_amount = fields.Decimal(required=True, places=2)
    dish_measure_unit = fields.String(required=True)
    dish_sum = fields.Decimal(required=True, places=2)
    dish_discount_sum = fields.Decimal(required=True, places=2)
    dish_return_sum = fields.Decimal(required=True, places=2)
    
    # Дополнительная информация
    increase_sum = fields.Decimal(required=True, places=2)
    increase_type = fields.String(allow_none=True)
    
    # Метаданные
    created_at = fields.DateTime(dump_only=True)

# Создаем экземпляры схем
iko_check_schema = IKOCheckSchema()
iko_checks_schema = IKOCheckSchema(many=True) 