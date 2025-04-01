from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class IKODocument(db.Model):
    __tablename__ = 'iko_documents'

    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(255), nullable=False)
    document_number_iko = db.Column(db.String(50), nullable=False)
    document_date_iko = db.Column(db.Date, nullable=False)
    warehouse_iko = db.Column(db.String(255), nullable=False)
    warehouse_code_iko = db.Column(db.String(50), nullable=False)
    operation_iko = db.Column(db.String(100), nullable=False)
    product_code_iko = db.Column(db.String(50), nullable=False)
    product_name_iko = db.Column(db.String(255), nullable=False)
    quantity_iko = db.Column(db.Numeric(15, 3), nullable=False)
    price_with_vat_iko = db.Column(db.Numeric(15, 2), nullable=False)
    amount_with_vat_iko = db.Column(db.Numeric(15, 2), nullable=False)
    vat_amount_iko = db.Column(db.Numeric(15, 2), nullable=False)
    vat_rate_iko = db.Column(db.Numeric(5, 2), nullable=False)
    cost_price_per_unit_without_vat_iko = db.Column(db.Numeric(15, 2), nullable=False)
    cost_price_without_vat_iko = db.Column(db.Numeric(15, 2), nullable=False)
    unit_of_measure_iko = db.Column(db.String(20), nullable=False)
    shift_number_iko = db.Column(db.Integer, nullable=False)
    cash_register_number_iko = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<IKODocument {self.document_number_iko}>"