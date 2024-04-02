from logging import warning
from uuid import uuid4
from datetime import datetime
from base64 import b64decode, b64encode
from infrastructure.firebase.firestore import Firestore


class Repository:

    def __init__(self):
        self.conn = Firestore()


    def get_by_id(self, repository: str, obj_id: str) -> dict | None:
        return self.conn.get_document_by_id(repository,  obj_id)


    def get_by_fields(
            self, repository: str, limit: int | None = None, created_before: datetime | None = None, 
            created_after: datetime | None = None, **kwargs
        ) -> list[dict]:
        return self.conn.get_documents_by_criteria(
            collection=repository, 
            limit=limit, 
            created_before=created_before, 
            created_after=created_after, 
            **kwargs
        )


    def page(self, repository: str, cursor: str | None = None, limit: int | None = None, **kwargs)-> tuple[str | None, list[dict]]:
        try:
            last_created = datetime.strptime(
                b64decode(cursor).decode("utf-8"), "%Y-%m-%d %H:%M:%S %z"
            ) if cursor else None
        except UnicodeDecodeError as e:
            warning(f"got cursor: {cursor} and failed to decode {e}")
            last_created = None

        new_cursor, data_list = self.conn.page_by_created(
            collection=repository, 
            limit=limit, 
            last_created=last_created,
            **kwargs
        )
        new_cursor = None if not new_cursor else b64encode(
            new_cursor.strftime("%Y-%m-%d %H:%M:%S %z").encode("utf-8")
        ).decode("utf-8")

        return new_cursor, data_list

    def get_all(self, repository: str) -> list[dict]:
        return self.conn.get_documents(repository)


    def save(self, repository: str,  dict_data: dict) -> dict:
        id = Repository.__generate_id()

        if self.conn.get_document_by_id(repository, id):
            raise Exception(f"duplicates uuids {id}")
        
        obj_dict = Repository.__remove_key(dict_data, "id")

        return self.conn.create_document(
            collection = repository,
            id = id,
            data = obj_dict,
        )
    

    def update(self, repository: str,  dict_data: dict) -> dict:
        dict_data_without_id = Repository.__remove_key(dict_data, "id")

        return self.conn.update_document(
            collection = repository,
            id = dict_data["id"],
            data = dict_data_without_id,
        )

    def delete(self, repository: str, obj_id: str) -> None:
        self.conn.delete_document(repository, obj_id)
    

    @staticmethod
    def __generate_id() -> str:
        return str(uuid4())

    
    @staticmethod
    def __remove_key(d: dict, key):
        r = dict(d)
        del r[key]
        return r
