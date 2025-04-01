from typing import Dict, List, Optional, Tuple
from sqlalchemy import or_
from models.iko_document import db, IKODocument

class IKODocumentService:
    @staticmethod
    def create_document(data: Dict) -> IKODocument:
        document = IKODocument(**data)
        db.session.add(document)
        db.session.commit()
        return document

    @staticmethod
    def get_document(document_id: int) -> Optional[IKODocument]:
        return IKODocument.query.get_or_404(document_id)

    @staticmethod
    def get_documents(page: int, per_page: int, filters: Dict = None) -> Tuple[List[IKODocument], int]:
        query = IKODocument.query

        if filters:
            if organization := filters.get('organization'):
                query = query.filter(IKODocument.organization.ilike(f"%{organization}%"))
            if department := filters.get('department'):
                query = query.filter(IKODocument.department.ilike(f"%{department}%"))
            if document_number := filters.get('document_number_iko'):
                query = query.filter(IKODocument.document_number_iko.ilike(f"%{document_number}%"))
            if warehouse := filters.get('warehouse_iko'):
                query = query.filter(IKODocument.warehouse_iko.ilike(f"%{warehouse}%"))
            if product_code := filters.get('product_code_iko'):
                query = query.filter(IKODocument.product_code_iko.ilike(f"%{product_code}%"))
            if search := filters.get('search'):
                query = query.filter(or_(
                    IKODocument.organization.ilike(f"%{search}%"),
                    IKODocument.product_name_iko.ilike(f"%{search}%"),
                    IKODocument.document_number_iko.ilike(f"%{search}%")
                ))

        total = query.count()
        documents = query.order_by(IKODocument.created_at.desc()) \
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        return documents.items, total

    @staticmethod
    def update_document(document_id: int, data: Dict) -> IKODocument:
        document = IKODocument.query.get_or_404(document_id)
        for key, value in data.items():
            setattr(document, key, value)
        db.session.commit()
        return document

    @staticmethod
    def delete_document(document_id: int) -> bool:
        document = IKODocument.query.get_or_404(document_id)
        db.session.delete(document)
        db.session.commit()
        return True