from datetime import datetime
from models import db
import uuid

class IKOCheck(db.Model):
    __tablename__ = 'sales_receipts'

    id = db.Column(db.Integer, primary_key=True)
    
    # Информация о кассе и подразделении
    cash_register_name = db.Column(db.String(255))
    cash_register_serial_number = db.Column(db.String(50))
    cash_register_number = db.Column(db.Integer)
    department_name = db.Column(db.String(255))
    department_id = db.Column(db.String(36))  # UUID хранится как строка
    store_name = db.Column(db.String(255))
    
    # Информация о чеке
    fiscal_cheque_number = db.Column(db.String(50))
    order_number = db.Column(db.Integer)
    close_time = db.Column(db.DateTime, nullable=False)
    precheque_time = db.Column(db.DateTime)
    order_type = db.Column(db.String(50))
    pay_types = db.Column(db.String(255))
    deleted_with_writeoff = db.Column(db.String(50))
    
    # Информация о товаре/блюде
    dish_code = db.Column(db.String(50))
    dish_name = db.Column(db.String(255))
    dish_amount = db.Column(db.Numeric(10, 2))
    dish_measure_unit = db.Column(db.String(50))
    dish_sum = db.Column(db.Numeric(10, 2))
    dish_discount_sum = db.Column(db.Numeric(10, 2))
    dish_return_sum = db.Column(db.Numeric(10, 2))
    
    # Дополнительная информация
    increase_sum = db.Column(db.Numeric(10, 2))
    increase_type = db.Column(db.String(100))
    
    # Метаданные
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<IKOCheck {self.fiscal_cheque_number}>' 