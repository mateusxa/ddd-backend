import uuid
from domain.entites.entity import Entity, EntityId
from infrastructure.firebase.firestore import Firestore


class Repository:

    def __init__(self):
        self.conn = Firestore()


    def get_by_id(self, obj: EntityId) -> dict | None:
        return self.conn.get_document_by_id(obj.get_class_name(),  obj.value)


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
        id = obj.id.value
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
        return str(uuid.uuid4())

    
    @staticmethod
    def __remove_key(d: dict, key):
        r = dict(d)
        del r[key]
        return r
    