from base64 import b64decode, b64encode
from datetime import datetime
from logging import warning
from typing import Any, Dict, List
from uuid import uuid4
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from infrastructure.firebase import Firebase
from utils.error import Error


class Firestore(Firebase):

    def __init__(self):
        self.client = firestore.client()

    def create(self, collection: str, data: dict) -> dict:
        id = Firestore.__generate_id()

        if self.get_by_id(collection=collection, id=id):
            raise Error(Error.Code.internal_error, f"duplicates uuids {id}", 500)
        
        data_without_id = Firestore.__remove_key(data, "id") if "id" in data else data

        self.client.collection(collection).document(id).set(data_without_id)
        data["id"] = id
        return data


    def update(self, collection: str, data: dict) -> dict:
        ref = self.client.collection(collection).document(data["id"])

        data_without_id = Firestore.__remove_key(data, "id")
        ref.update(data_without_id)
        
        updated_data = self.get_by_id(collection=collection, id=data["id"])
        if not updated_data:
            raise Error(Error.Code.internal_error, f"Document updated but could not be found! {collection}/{data['id']}", 500)
        return updated_data

    def get_by_id(self, collection: str, id: str) -> dict | None:
        doc_ref = self.client.collection(collection).document(id)
        data = doc_ref.get().to_dict()
        if data:
            data["id"] = id
            return data
        return None


    def get_all(self, collection: str) -> List[Dict[str, Any]]:
        docs = self.client.collection(collection).stream()

        query_result: List[Dict[str, Any]] = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if doc_dict:
                doc_dict["id"] = doc.id
                query_result.append(doc_dict)

        return query_result
    

    def get_by_fields(self, collection: str, limit: int | None = None, **kwargs) -> list[Dict[str, Any]]:
        query = self.client.collection(collection)

        for key, value in kwargs.items():
            if value:
                query = query.where(filter=FieldFilter(key, '==', value))
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
    

    def page(self, collection: str, cursor: str | None = None, limit: int | None = None, **kwargs):
        try:
            last_created = datetime.strptime(
                b64decode(cursor).decode("utf-8"), "%Y-%m-%d %H:%M:%S %z"
            ) if cursor else None
        except UnicodeDecodeError as e:
            warning(f"got cursor: {cursor} and failed to decode {e}")
            last_created = None

        ref = self.client.collection(collection)
        query = ref.order_by("created", direction=firestore.Query.DESCENDING)

        for key, value in kwargs.items():
            if value:
                query = query.where(filter=FieldFilter(key, '==', value))
        
        if limit:
            query = query.limit(limit)

        if last_created:
            query = query.start_after({"created": last_created})

        docs = query.stream()
        docs_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if doc_dict:
                doc_dict["id"] = doc.id
                docs_list.append(doc_dict)

        last_doc = None if len(docs_list) == 0 else docs_list[-1]
        last_pop: datetime | None = None if not last_doc else last_doc["created"]

        new_cursor = None if not last_pop else b64encode(
            last_pop.strftime("%Y-%m-%d %H:%M:%S %z").encode("utf-8")
        ).decode("utf-8")

        return new_cursor, docs_list


    def delete(self, collection: str, id: str):
        self.client.collection(collection).document(id).delete()


    @staticmethod
    def __remove_key(d: dict, key):
        r = dict(d)
        del r[key]
        return r


    @staticmethod
    def __generate_id() -> str:
        return str(uuid4())