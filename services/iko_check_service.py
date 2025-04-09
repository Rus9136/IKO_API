from models.iko_check import IKOCheck
from schemas.iko_check_schema import iko_check_schema, iko_checks_schema
from datetime import datetime
from sqlalchemy import func
from models.iko_document import db

class IKOCheckService:
    @staticmethod
    def create_check(data):
        """Создание нового чека"""
        try:
            # Валидация данных
            validated_data = iko_check_schema.load(data)
            
            # Создание нового чека
            new_check = IKOCheck(**validated_data)
            
            # Сохранение в базу данных
            db.session.add(new_check)
            db.session.commit()
            
            return iko_check_schema.dump(new_check)
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_checks(page=1, per_page=20, start_date=None, end_date=None):
        """Получение списка чеков с пагинацией и фильтрацией по дате"""
        query = IKOCheck.query
        
        # Применяем фильтры по дате
        if start_date:
            query = query.filter(IKOCheck.close_time >= start_date)
        if end_date:
            query = query.filter(IKOCheck.close_time <= end_date)
        
        # Сортируем по дате закрытия чека
        query = query.order_by(IKOCheck.close_time.desc())
        
        # Применяем пагинацию
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': iko_checks_schema.dump(pagination.items),
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }

    @staticmethod
    def get_check_by_id(check_id):
        """Получение чека по ID"""
        check = IKOCheck.query.get(check_id)
        if not check:
            return None
        return iko_check_schema.dump(check)

    @staticmethod
    def get_statistics(start_date=None, end_date=None):
        """Получение статистики по чекам"""
        query = db.session.query(
            func.count(IKOCheck.id).label('total_checks'),
            func.sum(IKOCheck.dish_sum).label('total_sum'),
            func.avg(IKOCheck.dish_sum).label('average_sum'),
            func.count(IKOCheck.dish_code.distinct()).label('unique_products')
        )
        
        if start_date:
            query = query.filter(IKOCheck.close_time >= start_date)
        if end_date:
            query = query.filter(IKOCheck.close_time <= end_date)
            
        result = query.first()
        
        return {
            'total_checks': result.total_checks or 0,
            'total_sum': float(result.total_sum or 0),
            'average_sum': float(result.average_sum or 0),
            'unique_products': result.unique_products or 0
        } 