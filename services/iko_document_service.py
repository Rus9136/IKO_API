from typing import Dict, List, Optional, Tuple
from sqlalchemy import or_
from models.iko_document import db, IKODocument
from datetime import datetime

class IKODocumentService:
    @staticmethod
    def create_document(data: Dict) -> IKODocument:
        document = IKODocument(**data)
        db.session.add(document)
        db.session.commit()
        return document

    @staticmethod
    def bulk_create_or_update_documents(documents_data: List[Dict]) -> List[IKODocument]:
        """Массовое создание или обновление документов"""
        result_documents = []
        
        for data in documents_data:
            # Поиск существующего документа по комбинации document_number_iko и product_code_iko
            existing_document = IKODocument.query.filter_by(
                document_number_iko=data['document_number_iko'],
                product_code_iko=data['product_code_iko']
            ).first()
            
            if existing_document:
                # Обновляем существующий документ
                for key, value in data.items():
                    setattr(existing_document, key, value)
                result_documents.append(existing_document)
            else:
                # Создаем новый документ
                new_document = IKODocument(**data)
                db.session.add(new_document)
                result_documents.append(new_document)
        
        db.session.commit()
        return result_documents

    @staticmethod
    def get_document(document_id: int) -> Optional[IKODocument]:
        return IKODocument.query.get_or_404(document_id)

    @staticmethod
    def get_documents(page: int, per_page: int, filters: Dict = None) -> Tuple[List[IKODocument], int]:
        query = IKODocument.query

        if filters:
            if organization := filters.get('organization'):
                query = query.filter(IKODocument.organization.ilike(f'%{organization}%'))
            if department := filters.get('department'):
                query = query.filter(IKODocument.department.ilike(f'%{department}%'))
            if document_number := filters.get('document_number'):
                query = query.filter(IKODocument.document_number_iko.ilike(f'%{document_number}%'))
            if warehouse := filters.get('warehouse'):
                query = query.filter(IKODocument.warehouse_iko.ilike(f'%{warehouse}%'))
            if product_code := filters.get('product_code'):
                query = query.filter(IKODocument.product_code_iko.ilike(f'%{product_code}%'))
            if search := filters.get('search'):
                search_term = f'%{search}%'
                query = query.filter(
                    db.or_(
                        IKODocument.organization.ilike(search_term),
                        IKODocument.department.ilike(search_term),
                        IKODocument.document_number_iko.ilike(search_term),
                        IKODocument.warehouse_iko.ilike(search_term),
                        IKODocument.product_code_iko.ilike(search_term),
                        IKODocument.product_name_iko.ilike(search_term)
                    )
                )
            if is_processed := filters.get('is_processed'):
                query = query.filter(IKODocument.is_processed == is_processed)
            if start_date := filters.get('start_date'):
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    query = query.filter(IKODocument.document_date_iko >= start_date)
                except ValueError:
                    pass
            if end_date := filters.get('end_date'):
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    query = query.filter(IKODocument.document_date_iko <= end_date)
                except ValueError:
                    pass

        total = query.count()
        documents = query.order_by(IKODocument.created_at.desc()) \
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        return documents.items, total

    @staticmethod
    def get_documents_by_ids(document_ids: List[int]) -> List[IKODocument]:
        """Получение документов по массиву ID"""
        return IKODocument.query.filter(IKODocument.id.in_(document_ids)).all()

    @staticmethod
    def update_document(document_id: int, data: Dict) -> IKODocument:
        document = IKODocument.query.get_or_404(document_id)
        for key, value in data.items():
            setattr(document, key, value)
        db.session.commit()
        return document

    @staticmethod
    def delete_document(document_id: int) -> None:
        document = IKODocument.query.get_or_404(document_id)
        db.session.delete(document)
        db.session.commit()

    @staticmethod
    def bulk_update_processed_status(document_ids: List[int], is_processed: bool) -> List[IKODocument]:
        documents = IKODocument.query.filter(IKODocument.id.in_(document_ids)).all()
        for document in documents:
            document.is_processed = is_processed
        db.session.commit()
        return documents

    @staticmethod
    def get_statistics() -> Dict:
        total_documents = IKODocument.query.count()
        processed_documents = IKODocument.query.filter_by(is_processed=True).count()
        unprocessed_documents = IKODocument.query.filter_by(is_processed=False).count()
        
        today = datetime.utcnow().date()
        documents_today = IKODocument.query.filter(
            db.func.date(IKODocument.created_at) == today
        ).count()

        return {
            "total_documents": total_documents,
            "processed_documents": processed_documents,
            "unprocessed_documents": unprocessed_documents,
            "documents_today": documents_today
        }

    @staticmethod
    def get_documents_by_date_range(start_date: datetime, end_date: datetime, 
                                  page: int, per_page: int) -> Tuple[List[IKODocument], int]:
        query = IKODocument.query.filter(
            IKODocument.document_date_iko.between(start_date, end_date)
        )
        
        total = query.count()
        documents = query.order_by(IKODocument.document_date_iko.desc()) \
                       .paginate(page=page, per_page=per_page, error_out=False)
        
        return documents.items, total

    @staticmethod
    def get_document_by_number_and_product(document_number: str, product_code: str) -> Optional[IKODocument]:
        """Получение документа по номеру документа и коду продукта"""
        return IKODocument.query.filter_by(
            document_number_iko=document_number,
            product_code_iko=product_code
        ).first()

    @staticmethod
    def get_all_documents(filters: Dict = None) -> List[IKODocument]:
        """Получение всех документов без пагинации"""
        query = IKODocument.query

        if filters:
            if organization := filters.get('organization'):
                query = query.filter(IKODocument.organization.ilike(f'%{organization}%'))
            if department := filters.get('department'):
                query = query.filter(IKODocument.department.ilike(f'%{department}%'))
            if document_number := filters.get('document_number'):
                query = query.filter(IKODocument.document_number_iko.ilike(f'%{document_number}%'))
            if warehouse := filters.get('warehouse'):
                query = query.filter(IKODocument.warehouse_iko.ilike(f'%{warehouse}%'))
            if product_code := filters.get('product_code'):
                query = query.filter(IKODocument.product_code_iko.ilike(f'%{product_code}%'))
            if search := filters.get('search'):
                search_term = f'%{search}%'
                query = query.filter(
                    db.or_(
                        IKODocument.organization.ilike(search_term),
                        IKODocument.department.ilike(search_term),
                        IKODocument.document_number_iko.ilike(search_term),
                        IKODocument.warehouse_iko.ilike(search_term),
                        IKODocument.product_code_iko.ilike(search_term),
                        IKODocument.product_name_iko.ilike(search_term)
                    )
                )
            if is_processed := filters.get('is_processed'):
                query = query.filter(IKODocument.is_processed == is_processed)
            if start_date := filters.get('start_date'):
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                    query = query.filter(IKODocument.document_date_iko >= start_date)
                except ValueError:
                    pass
            if end_date := filters.get('end_date'):
                try:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                    query = query.filter(IKODocument.document_date_iko <= end_date)
                except ValueError:
                    pass

        return query.order_by(IKODocument.created_at.desc()).all()