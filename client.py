import requests
from datetime import date
from typing import Dict, Optional
import json

class IKOApiClient:
    def __init__(self, base_url: str = "http://localhost:5000/api/v1"):
        self.base_url = base_url

    def create_document(self, document_data: Dict) -> Dict:
        """Create a new IKO document."""
        response = requests.post(f"{self.base_url}/documents", json=document_data)
        response.raise_for_status()
        return response.json()

    def get_documents(self, page: int = 1, per_page: int = 20, filters: Optional[Dict] = None) -> Dict:
        """Get a list of IKO documents with optional filtering."""
        params = {'page': page, 'per_page': per_page}
        if filters:
            params.update(filters)
        
        response = requests.get(f"{self.base_url}/documents", params=params)
        response.raise_for_status()
        return response.json()

    def get_document(self, document_id: int) -> Dict:
        """Get a single IKO document by ID."""
        response = requests.get(f"{self.base_url}/documents/{document_id}")
        response.raise_for_status()
        return response.json()

    def update_document(self, document_id: int, document_data: Dict) -> Dict:
        """Update an existing IKO document."""
        response = requests.put(f"{self.base_url}/documents/{document_id}", json=document_data)
        response.raise_for_status()
        return response.json()

    def delete_document(self, document_id: int) -> None:
        """Delete an IKO document."""
        response = requests.delete(f"{self.base_url}/documents/{document_id}")
        response.raise_for_status()

def main():
    # Create API client instance
    client = IKOApiClient()

    # Example document data
    sample_document = {
        "organization": "Sample Corp",
        "department": "Warehouse 1",
        "document_number_iko": "DOC-2025-001",
        "document_date_iko": str(date.today()),
        "warehouse_iko": "Main Warehouse",
        "warehouse_code_iko": "WH001",
        "operation_iko": "Receipt",
        "product_code_iko": "PRD001",
        "product_name_iko": "Sample Product",
        "quantity_iko": "10.000",
        "price_with_vat_iko": "120.00",
        "amount_with_vat_iko": "1200.00",
        "vat_amount_iko": "200.00",
        "vat_rate_iko": "20.00",
        "cost_price_per_unit_without_vat_iko": "80.00",
        "cost_price_without_vat_iko": "800.00",
        "unit_of_measure_iko": "PCS",
        "shift_number_iko": 1,
        "cash_register_number_iko": "REG001"
    }

    try:
        # Create a new document
        print("Creating new document...")
        created_doc = client.create_document(sample_document)
        print(f"Created document: {json.dumps(created_doc, indent=2)}")

        # Get the created document
        doc_id = created_doc['id']
        print(f"\nRetrieving document {doc_id}...")
        retrieved_doc = client.get_document(doc_id)
        print(f"Retrieved document: {json.dumps(retrieved_doc, indent=2)}")

        # Update the document
        update_data = {
            "quantity_iko": "15.000",
            "amount_with_vat_iko": "1800.00"
        }
        print(f"\nUpdating document {doc_id}...")
        updated_doc = client.update_document(doc_id, update_data)
        print(f"Updated document: {json.dumps(updated_doc, indent=2)}")

        # Get list of documents with filters
        print("\nRetrieving filtered documents...")
        filters = {
            "organization": "Sample",
            "page": 1,
            "per_page": 10
        }
        documents_list = client.get_documents(filters=filters)
        print(f"Retrieved documents: {json.dumps(documents_list, indent=2)}")

        # Delete the document
        print(f"\nDeleting document {doc_id}...")
        client.delete_document(doc_id)
        print("Document deleted successfully")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()