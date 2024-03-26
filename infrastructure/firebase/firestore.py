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
    

    def page_by_created(self, collection: str, limit: int | None = None, last_created: datetime | None = None, **kwargs):
        ref = self.client.collection(collection)
        query = ref.order_by("created", direction=firestore.Query.DESCENDING)

        for key, value in kwargs.items():
            if value:
                query = query.where(key, '==', value)
        
        if limit:
            query = query.limit(limit)

        if last_created:
            query = query.start_after({"created": last_created})


        docs = query.stream()
        docs_list = [doc.to_dict() for doc in docs]
        last_doc = None if len(docs_list) == 0 else docs_list[-1]
        last_pop = None if not last_doc else last_doc["created"]

        return last_pop, docs_list


    def delete_document(self, collection: str, id: str):
        self.client.collection(collection).document(id).delete()
