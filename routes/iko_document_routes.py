from flask import Blueprint, request, jsonify, make_response
from marshmallow import ValidationError
from services.iko_document_service import IKODocumentService
from schemas.iko_document_schema import iko_document_schema, iko_documents_schema
from config import Config
from datetime import datetime
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('iko_documents', __name__)

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@bp.route('/documents', methods=['POST', 'OPTIONS'])
def create_document():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        logger.debug(f"Received request data: {request.json}")
        data = iko_document_schema.load(request.json)
        logger.debug(f"Validated data: {data}")
        document = IKODocumentService.create_document(data)
        logger.debug(f"Created document: {document}")
        response = jsonify(iko_document_schema.dump(document))
        return add_cors_headers(response), 201
    except ValidationError as e:
        logger.error(f"Validation error: {e.messages}")
        response = jsonify({"message": "Validation error", "errors": e.messages})
        return add_cors_headers(response), 400
    except Exception as e:
        logger.error(f"Error creating document: {str(e)}", exc_info=True)
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents', methods=['GET', 'OPTIONS'])
def get_documents():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        filters = {
            'organization': request.args.get('organization'),
            'department': request.args.get('department'),
            'document_number_iko': request.args.get('document_number'),
            'warehouse_iko': request.args.get('warehouse'),
            'product_code_iko': request.args.get('product_code'),
            'search': request.args.get('search'),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'is_processed': request.args.get('is_processed')
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        logger.debug(f"Applied filters: {filters}")
        documents, total = IKODocumentService.get_documents(page, per_page, filters)
        
        response = jsonify({
            'items': iko_documents_schema.dump(documents),
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
        return add_cors_headers(response)
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}", exc_info=True)
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/<int:document_id>', methods=['GET', 'OPTIONS'])
def get_document(document_id):
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        document = IKODocumentService.get_document(document_id)
        response = jsonify(iko_document_schema.dump(document))
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/<int:document_id>', methods=['PUT', 'OPTIONS'])
def update_document(document_id):
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        data = iko_document_schema.load(request.json)
        document = IKODocumentService.update_document(document_id, data)
        response = jsonify(iko_document_schema.dump(document))
        return add_cors_headers(response)
    except ValidationError as e:
        response = jsonify({"message": "Validation error", "errors": e.messages})
        return add_cors_headers(response), 400
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/<int:document_id>', methods=['DELETE', 'OPTIONS'])
def delete_document(document_id):
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        IKODocumentService.delete_document(document_id)
        response = jsonify({"message": "Document deleted successfully"})
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/bulk-process', methods=['POST', 'OPTIONS'])
def bulk_process_documents():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        data = request.json
        if isinstance(data, list):
            document_ids = data
            is_processed = True
        else:
            document_ids = data.get('document_ids', [])
            is_processed = data.get('is_processed', True)
        
        documents = IKODocumentService.bulk_update_processed_status(document_ids, is_processed)
        response = jsonify({
            'message': 'Documents updated successfully',
            'documents': iko_documents_schema.dump(documents)
        })
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/statistics', methods=['GET', 'OPTIONS'])
def get_statistics():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        stats = IKODocumentService.get_statistics()
        response = jsonify(stats)
        return add_cors_headers(response)
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/by-date-range', methods=['GET', 'OPTIONS'])
def get_documents_by_date_range():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        
        documents, total = IKODocumentService.get_documents_by_date_range(
            start_date, end_date, page, per_page
        )
        
        response = jsonify({
            'items': iko_documents_schema.dump(documents),
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
        return add_cors_headers(response)
    except ValueError:
        response = jsonify({"message": "Invalid date format. Use YYYY-MM-DD"})
        return add_cors_headers(response), 400
    except Exception as e:
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/bulk', methods=['POST', 'OPTIONS'])
def get_documents_bulk():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        data = request.json
        if not data or 'document_ids' not in data:
            response = jsonify({"message": "document_ids is required"})
            return add_cors_headers(response), 400
            
        document_ids = data['document_ids']
        if not isinstance(document_ids, list):
            response = jsonify({"message": "document_ids must be an array"})
            return add_cors_headers(response), 400
            
        documents = IKODocumentService.get_documents_by_ids(document_ids)
        response = jsonify({
            'items': iko_documents_schema.dump(documents),
            'total': len(documents)
        })
        return add_cors_headers(response)
    except Exception as e:
        logger.error(f"Error getting documents bulk: {str(e)}", exc_info=True)
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500

@bp.route('/documents/all', methods=['GET', 'OPTIONS'])
def get_all_documents():
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
        
    try:
        filters = {
            'organization': request.args.get('organization'),
            'department': request.args.get('department'),
            'document_number': request.args.get('document_number'),
            'warehouse': request.args.get('warehouse'),
            'product_code': request.args.get('product_code'),
            'search': request.args.get('search'),
            'start_date': request.args.get('start_date'),
            'end_date': request.args.get('end_date'),
            'is_processed': request.args.get('is_processed')
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        logger.debug(f"Applied filters: {filters}")
        documents = IKODocumentService.get_all_documents(filters)
        
        response = jsonify({
            'items': iko_documents_schema.dump(documents),
            'total': len(documents)
        })
        return add_cors_headers(response)
    except Exception as e:
        logger.error(f"Error getting all documents: {str(e)}", exc_info=True)
        response = jsonify({"message": "An error occurred", "error": str(e)})
        return add_cors_headers(response), 500