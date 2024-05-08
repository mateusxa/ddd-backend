from domain.entites.admin import Admin
from utils.error import Error
from infrastructure.repository import Repository
from infrastructure.models.sqlalchemy.admin import AdminModel
from infrastructure.data_mapper.sqlalchemy.admin import admin_entity_to_model, admin_model_to_entity


class AdminRepository(Repository):

    entity_name: str

    def __init__(self):
        super().__init__()
        self.entity_name = "admins"
        

    def create(self, admin: Admin) -> Admin:
        instance = admin_entity_to_model(admin)
        self.session.add(instance)
        self.session.commit()
        return admin_model_to_entity(instance)
        

    def get_by_id(self, admin_id: str) -> Admin | None:
        instance = self.session.get(AdminModel, admin_id)
        if not instance:
            return None
        return admin_model_to_entity(instance)


    def get_by_email(self, email) -> Admin | None:
        instance = self.session.query(AdminModel).filter_by(email=email).first()
        if not instance:
            return None
        return admin_model_to_entity(instance)

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Admin]]:
        admin_id = self.decode_cursor(cursor)
        instances = self.session.query(AdminModel).filter_by(id=admin_id).limit(limit).all()
        
        new_cursor = None
        admin_list = []
        for instance in instances:
            admin = admin_model_to_entity(instance)
            admin_list.append(admin)
            if not admin.id:
                raise Error(Error.Code.internal_error, "Mapped admin without id", 500)
            new_cursor = admin.id

        new_cursor = self.encode_cursor(new_cursor)
        return new_cursor,  admin_list


    def update(self, admin: Admin) -> Admin:
        if not admin.id:
            # TODO fix error  
            raise Error("update", "update")
        
        instance = self.session.get(AdminModel, admin.id)
        if not instance:
            # TODO fix error
            raise Error("not exists", "object not exists")
        
        instance.name = admin.name
        instance.password = admin.password
        self.session.commit()
        return admin_model_to_entity(instance)


    def delete(self, admin_id: str) -> None:
        admin_model = self.session.get(AdminModel, admin_id)
        self.session.delete(admin_model)   
        self.session.commit()

    
    def __getitem__(self, key):
        return self.get_by_id(key)
    