import firebase_admin
from firebase_admin import credentials, firestore


class FirestoreService:

    firebase_admin.initialize_app(credentials.Certificate("repository/credentials.json"))
    client = firestore.client()

    def create_document(self, collection: str, id: str, data: dict) -> dict:
        self.client.collection(collection).document(id).set(data)
        data["id"] = id
        return data


    def get_document_by_id(self, collection: str, id: str) -> dict | None:
        doc_ref = self.client.collection(collection).document(id)
        data = doc_ref.get().to_dict()
        if data:
            data["id"] = id
            return data
        return None


    def get_documents(self, collection: str):
        docs = self.client.collection(collection).stream()

        final_doc_list = []
        for doc in docs:
            doc_dict = doc.to_dict()
            if doc_dict:
                doc_dict["id"] = doc.id
                final_doc_list.append(doc_dict)

        return final_doc_list


    def delete_document(self, collection: str, id: str):
        self.client.collection(collection).document(id).delete()
