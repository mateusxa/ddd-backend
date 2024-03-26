from datetime import datetime
from typing import Any, Dict, List
from firebase_admin import firestore
from infrastructure.firebase import Firebase


class Firestore(Firebase):

    client = firestore.client()


    def create_document(self, collection: str, id: str, data: dict) -> dict:
        self.client.collection(collection).document(id).set(data)
        data["id"] = id
        return data

    def update_document(self, collection: str, id: str, data: dict) -> dict:
        ref = self.client.collection(collection).document(id)
        ref.update(data)
        updated_data = self.get_document_by_id(collection=collection, id=id)
        if not updated_data:
            raise Exception(f"Document updated but could not found! {collection}/{id}")
        return updated_data

    def get_document_by_id(self, collection: str, id: str) -> dict | None:
        doc_ref = self.client.collection(collection).document(id)
        data = doc_ref.get().to_dict()
        if data:
            data["id"] = id
            return data
        return None


    def get_documents(self, collection: str) -> List[Dict[str, Any]]:
        docs = self.client.collection(collection).stream()

        query_result: List[Dict[str, Any]] = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if doc_dict:
                doc_dict["id"] = doc.id
                query_result.append(doc_dict)

        return query_result
    

    def get_documents_by_criteria(
        self, collection: str, limit: int | None = None, created_before: datetime | None = None, 
        created_after: datetime | None = None, **kwargs
    ) -> list[Dict[str, Any]]:
        query = self.client.collection(collection)

        for key, value in kwargs.items():
            if value:
                query = query.where(key, '==', value)

        if created_before:
            query = query.where('created_at', '<=', created_before).order_by('created_at')
        if created_after:
            query = query.where('created_at', '>=', created_after).order_by('created_at')
        if limit:
            query = query.limit(limit)

        results = query.stream()

        query_result: List[Dict[str, Any]] = []
        for doc in results:
            doc_dict = doc.to_dict()
            if doc_dict:
                doc_dict["id"] = doc.id
                query_result.append(doc_dict)
        return query_result

    # TODO testar esses dois aqui
    def page_documents_by_criteria(
        self, collection: str, limit: int, start_after: str | None = None, **kwargs
    ) -> tuple[ str | None, list[Dict[str, Any]] ]:
        query = self.client.collection(collection)

        for key, value in kwargs.items():
            if value:
                query = query.where(key, '==', value)

        if start_after:
            start_doc_ref = self.client.collection('your_collection').document(start_after)
            query = query.start_after({'__name__': start_doc_ref.id})  

        query = query.order_by('created')
        query = query.limit(limit)

        # Execute the query
        docs = query.stream()

        # Extract data from documents
        last_doc_id: str | None = None
        documents = []
        for doc in docs:
            document = doc.to_dict()
            if document:
                document["id"] = doc.id
                documents.append(document)
                last_doc_id = doc.id

        return last_doc_id, documents


    def delete_document(self, collection: str, id: str):
        self.client.collection(collection).document(id).delete()
