from uuid import uuid4
from datetime import datetime
from base64 import b64decode, b64encode
from domain.entites.entity import Entity, EntityId
from infrastructure.firebase.firestore import Firestore


class Repository:

    def __init__(self):
        self.conn = Firestore()


    def get_by_id(self, obj: EntityId) -> dict | None:
        return self.conn.get_document_by_id(obj.get_class_name(),  obj.value)


    def get_by_fields(self, database, limit: int | None = None, created_before: datetime | None = None, created_after: datetime | None = None, **kwargs):
        return self.conn.get_documents_by_criteria(collection=database, limit=limit, created_before=created_before, created_after=created_after, **kwargs)


    def page(self, database, cursor: str | None = None, limit: int | None = None, **kwargs):
        last_created = datetime.fromtimestamp(
            float(b64decode(cursor.encode("utf-8")).decode("utf-8"))
        ) if cursor else None
        new_cursor, data_list = self.conn.page_by_created(collection=database, limit=limit, last_created=last_created, **kwargs)
        new_cursor = b64encode(
            str(new_cursor.timestamp()).encode("utf-8")
        ).decode("utf-8") if new_cursor else None

        return new_cursor, data_list

    def get_all(self, obj: Entity):
        return self.conn.get_documents(obj.get_class_name())


    def save(self, obj: Entity) -> dict:
        id = Repository.__generate_id()
        class_name = obj.get_class_name()

        if self.conn.get_document_by_id(class_name, id):
            raise Exception(f"duplicates uuids {id}")
        
        obj_dict = Repository.__remove_key(obj.to_dict(), "id")

        return self.conn.create_document(
            collection = class_name,
            id = id,
            data = obj_dict,
        )
    

    def update(self, obj: Entity) -> dict:
        obj_dict = Repository.__remove_key(obj.to_dict(), "id")

        return self.conn.update_document(
            collection = obj.get_class_name(),
            id = obj.id.value,
            data = obj_dict,
        )

    def delete(self, obj: EntityId) -> None:
        self.conn.delete_document(obj.get_class_name(), obj.value)
    

    @staticmethod
    def __generate_id() -> str:
        return str(uuid4())

    
    @staticmethod
    def __remove_key(d: dict, key):
        r = dict(d)
        del r[key]
        return r
    