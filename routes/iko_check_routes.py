from flask import Blueprint, request
from services.iko_check_service import IKOCheckService
from flask_restx import Resource, Namespace, fields
from datetime import datetime

# Создаем Blueprint для маршрутов чеков
check_bp = Blueprint('checks', __name__)

# Создаем Namespace для Swagger документации
api = Namespace('checks', description='Операции с чеками')

# Определяем модели для Swagger
check_item = api.model('CheckItem', {
    'name': fields.String(required=True, description='Название товара'),
    'quantity': fields.Float(required=True, description='Количество'),
    'price': fields.Float(required=True, description='Цена')
})

check_model = api.model('Check', {
    'cash_register_name': fields.String(required=True, description='Название кассы'),
    'cash_register_serial_number': fields.String(required=True, description='Серийный номер кассы'),
    'cash_register_number': fields.Integer(required=True, description='Номер кассы'),
    'department_name': fields.String(required=True, description='Название подразделения'),
    'department_id': fields.String(required=True, description='ID подразделения (UUID)'),
    'store_name': fields.String(required=True, description='Название магазина'),
    'fiscal_cheque_number': fields.String(required=True, description='Фискальный номер чека'),
    'order_number': fields.Integer(required=True, description='Номер заказа'),
    'close_time': fields.DateTime(required=True, description='Время закрытия чека'),
    'precheque_time': fields.DateTime(description='Время предварительного чека'),
    'order_type': fields.String(description='Тип заказа'),
    'pay_types': fields.String(required=True, description='Типы оплаты'),
    'deleted_with_writeoff': fields.String(description='Статус удаления'),
    'dish_code': fields.String(required=True, description='Код товара'),
    'dish_name': fields.String(required=True, description='Название товара'),
    'dish_amount': fields.Float(required=True, description='Количество товара'),
    'dish_measure_unit': fields.String(required=True, description='Единица измерения'),
    'dish_sum': fields.Float(required=True, description='Сумма по товару'),
    'dish_discount_sum': fields.Float(required=True, description='Сумма скидки'),
    'dish_return_sum': fields.Float(required=True, description='Сумма возврата'),
    'increase_sum': fields.Float(required=True, description='Сумма увеличения'),
    'increase_type': fields.String(description='Тип увеличения')
})

@api.route('/')
class CheckList(Resource):
    @api.doc('list_checks')
    @api.param('page', 'Номер страницы', type=int, default=1)
    @api.param('per_page', 'Количество чеков на странице', type=int, default=20)
    @api.param('start_date', 'Начальная дата (YYYY-MM-DD)')
    @api.param('end_date', 'Конечная дата (YYYY-MM-DD)')
    def get(self):
        """Получение списка чеков"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
        return IKOCheckService.get_checks(page, per_page, start_date, end_date)

    @api.doc('create_check')
    @api.expect(check_model)
    def post(self):
        """Создание нового чека"""
        data = request.get_json()
        return IKOCheckService.create_check(data)

@api.route('/<int:check_id>')
class Check(Resource):
    @api.doc('get_check')
    def get(self, check_id):
        """Получение чека по ID"""
        check = IKOCheckService.get_check_by_id(check_id)
        if not check:
            api.abort(404, f"Чек с ID {check_id} не найден")
        return check

@api.route('/statistics')
class CheckStatistics(Resource):
    @api.doc('get_statistics')
    @api.param('start_date', 'Начальная дата (YYYY-MM-DD)')
    @api.param('end_date', 'Конечная дата (YYYY-MM-DD)')
    def get(self):
        """Получение статистики по чекам"""
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
        return IKOCheckService.get_statistics(start_date, end_date) 