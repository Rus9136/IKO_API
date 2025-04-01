from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from services.iko_document_service import IKODocumentService
from schemas.iko_document_schema import iko_document_schema, iko_documents_schema
from config import Config

bp = Blueprint('iko_documents', __name__)

@bp.route('/documents', methods=['POST'])
def create_document():
    try:
        data = iko_document_schema.load(request.json)
        document = IKODocumentService.create_document(data)
        return jsonify(iko_document_schema.dump(document)), 201
    except ValidationError as e:
        return jsonify({"message": "Validation error", "errors": e.messages}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@bp.route('/documents', methods=['GET'])
def get_documents():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', Config.ITEMS_PER_PAGE))
        filters = {
            'organization': request.args.get('organization'),
            'department': request.args.get('department'),
            'document_number_iko': request.args.get('document_number'),
            'warehouse_iko': request.args.get('warehouse'),
            'product_code_iko': request.args.get('product_code'),
            'search': request.args.get('search')
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        documents, total = IKODocumentService.get_documents(page, per_page, filters)
        
        return jsonify({
            'items': iko_documents_schema.dump(documents),
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@bp.route('/documents/<int:document_id>', methods=['GET'])
def get_document(document_id):
    try:
        document = IKODocumentService.get_document(document_id)
        return jsonify(iko_document_schema.dump(document))
    except Exception as e:
        return jsonify({"message": "Document not found", "error": str(e)}), 404

@bp.route('/documents/<int:document_id>', methods=['PUT'])
def update_document(document_id):
    try:
        data = iko_document_schema.load(request.json, partial=True)
        document = IKODocumentService.update_document(document_id, data)
        return jsonify(iko_document_schema.dump(document))
    except ValidationError as e:
        return jsonify({"message": "Validation error", "errors": e.messages}), 400
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@bp.route('/documents/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    try:
        IKODocumentService.delete_document(document_id)
        return '', 204
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500