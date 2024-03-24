import uuid
from typing import Protocol

from repository.firestore import FirestoreService


class Entity(Protocol):
    def to_dict(self) -> dict:
        ...


class Repository:

    def __init__(self):
        self.conn = FirestoreService()


    def get_by_id(self, obj: object) -> dict | None:
        return self.conn.get_document_by_id(Repository.__get_class_name_by_id(obj),  str(obj))


    def get_all(self, obj: object):
        return self.conn.get_documents(Repository.__get_class_name(obj))


    def save(self, obj: Entity) -> dict:
        id = Repository.__generate_id()
        class_name = Repository.__get_class_name(obj)

        if self.conn.get_document_by_id(class_name, id):
            raise Exception(f"duplicates uuids {id}")
        
        obj_dict = obj.to_dict()
        del obj_dict["id"]

        return self.conn.create_document(
            collection = class_name,
            id = id,
            data = obj.to_dict(),
        )


    def delete(self, obj: object) -> None:
        self.conn.delete_document(Repository.__get_class_name_by_id(obj), str(obj))
    

    @staticmethod
    def __generate_id() -> str:
        return str(uuid.uuid4())
    

    @staticmethod
    def __get_class_name(obj: object):
        return Repository.__get_plural_name(obj.__class__.__name__.lower())
    

    @staticmethod
    def __get_class_name_by_id(obj: object):
        return Repository.__get_plural_name(obj.__class__.__name__.lower()[:-2])
    

    @staticmethod
    def __get_plural_name(name: str):
        return name + "s" if name[-1] != "y" else name[:-1] + "ies"
