from flask_restx import Api, Resource, fields, reqparse
from flask import Blueprint
from datetime import date
from routes.iko_document_routes import document_api
from routes.iko_check_routes import check_api

# Создаем Blueprint для API документации
api_bp = Blueprint('api', __name__)

# Создаем API с Swagger документацией
api = Api(
    api_bp,
    version='1.0',
    title='IKO API',
    description='API для работы с документами и чеками',
    doc='/docs'
)

# Добавляем Namespace'ы
api.add_namespace(document_api)
api.add_namespace(check_api)

# Определяем пространство имен
ns = api.namespace('api/v1/documents', description='Операции с документами')

# Модели для документации
document_model = api.model('Document', {
    'id': fields.Integer(readonly=True, description='Уникальный идентификатор документа'),
    'organization': fields.String(required=True, description='Название организации'),
    'department': fields.String(required=True, description='Отдел'),
    'document_number_iko': fields.String(required=True, description='Номер документа'),
    'document_date_iko': fields.Date(required=True, description='Дата документа'),
    'warehouse_iko': fields.String(required=True, description='Название склада'),
    'warehouse_code_iko': fields.String(required=True, description='Код склада'),
    'operation_iko': fields.String(required=True, description='Тип операции'),
    'product_code_iko': fields.String(required=True, description='Код продукта'),
    'product_name_iko': fields.String(required=True, description='Название продукта'),
    'quantity_iko': fields.Float(required=True, description='Количество'),
    'price_with_vat_iko': fields.Float(required=True, description='Цена с НДС'),
    'amount_with_vat_iko': fields.Float(required=True, description='Сумма с НДС'),
    'vat_amount_iko': fields.Float(required=True, description='Сумма НДС'),
    'vat_rate_iko': fields.Float(required=True, description='Ставка НДС'),
    'cost_price_per_unit_without_vat_iko': fields.Float(required=True, description='Себестоимость за единицу без НДС'),
    'cost_price_without_vat_iko': fields.Float(required=True, description='Общая себестоимость без НДС'),
    'unit_of_measure_iko': fields.String(required=True, description='Единица измерения'),
    'shift_number_iko': fields.Integer(required=True, description='Номер смены'),
    'cash_register_number_iko': fields.String(required=True, description='Номер кассы'),
    'is_processed': fields.Boolean(description='Признак обработки документа'),
    'created_at': fields.DateTime(readonly=True, description='Дата создания записи'),
    'updated_at': fields.DateTime(readonly=True, description='Дата обновления записи')
})

# Модель для ответа со списком документов
documents_list_model = api.model('DocumentsList', {
    'items': fields.List(fields.Nested(document_model)),
    'total': fields.Integer(description='Общее количество документов'),
    'page': fields.Integer(description='Текущая страница'),
    'per_page': fields.Integer(description='Количество документов на странице'),
    'pages': fields.Integer(description='Общее количество страниц')
})

# Модель для массового получения документов
bulk_get_model = api.model('BulkGet', {
    'document_ids': fields.List(fields.Integer, required=True, description='Список ID документов для получения')
})

# Модель для массового обновления статуса
bulk_update_model = api.model('BulkUpdate', {
    'document_ids': fields.List(fields.Integer, required=True, description='Список ID документов'),
    'is_processed': fields.Boolean(required=True, description='Новый статус обработки')
})

# Модель для статистики
statistics_model = api.model('Statistics', {
    'total_documents': fields.Integer(description='Общее количество документов'),
    'processed_documents': fields.Integer(description='Количество обработанных документов'),
    'unprocessed_documents': fields.Integer(description='Количество необработанных документов'),
    'documents_today': fields.Integer(description='Количество документов за сегодня')
})

# Модель для массового создания/обновления документов
bulk_create_model = api.model('BulkCreate', {
    'message': fields.String(description='Сообщение о результате операции'),
    'items': fields.List(fields.Nested(document_model), description='Созданные или обновленные документы'),
    'total': fields.Integer(description='Общее количество обработанных документов')
})

# Модель для массового удаления документов
bulk_delete_model = api.model('BulkDelete', {
    'message': fields.String(description='Сообщение о результате операции'),
    'deleted_count': fields.Integer(description='Количество удаленных документов')
})

# Парсеры для параметров запроса
list_parser = reqparse.RequestParser()
list_parser.add_argument('page', type=int, default=1, help='Номер страницы')
list_parser.add_argument('per_page', type=int, default=20, help='Количество элементов на странице')
list_parser.add_argument('organization', type=str, help='Фильтр по организации')
list_parser.add_argument('department', type=str, help='Фильтр по отделу')
list_parser.add_argument('document_number', type=str, help='Фильтр по номеру документа')
list_parser.add_argument('warehouse', type=str, help='Фильтр по складу')
list_parser.add_argument('product_code', type=str, help='Фильтр по коду продукта')
list_parser.add_argument('search', type=str, help='Поиск по всем полям')
list_parser.add_argument('start_date', type=str, help='Начальная дата (YYYY-MM-DD)')
list_parser.add_argument('end_date', type=str, help='Конечная дата (YYYY-MM-DD)')
list_parser.add_argument('is_processed', type=bool, help='Фильтр по статусу обработки')

@ns.route('/')
class DocumentList(Resource):
    @ns.doc('list_documents')
    @ns.expect(list_parser)
    @ns.marshal_with(documents_list_model)
    def get(self):
        """Получить список документов с фильтрацией и пагинацией"""
        pass

    @ns.doc('create_document')
    @ns.expect(document_model)
    @ns.marshal_with(document_model, code=201)
    def post(self):
        """Создать новый документ"""
        pass

@ns.route('/bulk')
class BulkGetDocuments(Resource):
    @ns.doc('get_documents_bulk')
    @ns.expect(bulk_get_model)
    @ns.marshal_with(documents_list_model)
    def post(self):
        """Получить документы по массиву ID"""
        pass

@ns.route('/<int:id>')
@ns.param('id', 'Идентификатор документа')
class Document(Resource):
    @ns.doc('get_document')
    @ns.marshal_with(document_model)
    def get(self, id):
        """Получить документ по ID"""
        pass

    @ns.doc('update_document')
    @ns.expect(document_model)
    @ns.marshal_with(document_model)
    def put(self, id):
        """Обновить документ"""
        pass

    @ns.doc('delete_document')
    @ns.response(204, 'Документ успешно удален')
    def delete(self, id):
        """Удалить документ"""
        pass

@ns.route('/bulk-process')
class BulkProcess(Resource):
    @ns.doc('bulk_process_documents')
    @ns.expect(bulk_update_model) 
    @ns.marshal_with(documents_list_model)
    def post(self):
        """Массовое обновление статуса обработки документов"""
        pass

@ns.route('/statistics')
class Statistics(Resource):
    @ns.doc('get_statistivfncs')
    @ns.marshal_with(statistics_model)
    def get(self):
        """Получить статистику по документам"""
        pass

@ns.route('/all')
class AllDocuments(Resource):
    @ns.doc('get_all_documents')
    @ns.expect(list_parser)
    @ns.marshal_with(documents_list_model)
    def get(self):
        """Получить все документы без пагинации"""
        pass

@ns.route('/bulk-create')
class BulkCreateDocuments(Resource):
    @ns.doc('bulk_create_documents',
            description='Массовое создание или обновление документов. Если документ с указанным номером и кодом продукта существует - он будет обновлен, иначе создан новый.',
            responses={
                201: 'Документы успешно созданы/обновлены',
                400: 'Ошибка валидации данных',
                500: 'Внутренняя ошибка сервера'
            })
    @ns.expect([document_model])
    @ns.marshal_with(bulk_create_model, code=201)
    def post(self):
        """Массовое создание или обновление документов"""
        from flask import request
        from services.iko_document_service import IKODocumentService
        from schemas.iko_document_schema import iko_document_schema, iko_documents_schema
        from marshmallow import ValidationError
        import logging
        
        logger = logging.getLogger(__name__)
        
        try:
            # Проверяем, что данные пришли в виде массива
            if not isinstance(request.json, list):
                return {
                    "message": "Request body must be an array of documents",
                    "error": "Invalid request format"
                }, 400

            # Валидируем каждый документ в массиве
            validated_documents = []
            for doc_data in request.json:
                try:
                    validated_data = iko_document_schema.load(doc_data)
                    validated_documents.append(validated_data)
                except ValidationError as e:
                    logger.error(f"Validation error for document: {e.messages}")
                    return {
                        "message": "Validation error",
                        "errors": e.messages,
                        "document": doc_data
                    }, 400

            # Создаем или обновляем документы
            documents = IKODocumentService.bulk_create_or_update_documents(validated_documents)
            
            return {
                'message': 'Documents processed successfully',
                'items': iko_documents_schema.dump(documents),
                'total': len(documents)
            }, 201

        except Exception as e:
            logger.error(f"Error in bulk create/update: {str(e)}", exc_info=True)
            return {
                "message": "An error occurred while processing documents",
                "error": str(e)
            }, 500

@ns.route('/bulk-delete')
class BulkDeleteDocuments(Resource):
    @ns.doc('bulk_delete_documents',
            description='Массовое удаление документов по списку ID',
            responses={
                200: 'Документы успешно удалены',
                400: 'Ошибка валидации данных',
                500: 'Внутренняя ошибка сервера'
            })
    @ns.expect(bulk_get_model)
    @ns.marshal_with(bulk_delete_model)
    def post(self):
        """Массовое удаление документов"""
        pass