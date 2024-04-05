from domain.entites.admin import Admin
from repository.reposity import Repository
from infrastructure.firebase.firestore import Firestore


class AdminRepository(Repository):

    entity_name: str

    def __init__(self):
        self.entity_name = "admins"
        self.db = Firestore()


    def create(self, admin: Admin) -> Admin:
        return Admin.from_dict(self.db.create(self.entity_name, admin.to_dict()))
        

    def get_by_id(self, admin_id: str) -> Admin | None:
        admin_dict = self.db.get_by_id(self.entity_name, admin_id)
        return Admin.from_dict(admin_dict) if admin_dict else None


    def get_by_fields(self, limit: int | None = None, **kwargs) -> list[Admin]:
        return [Admin.from_dict(admin_dict) for admin_dict in self.db.get_by_fields(self.entity_name, limit=limit, **kwargs)]

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Admin]]:
        new_cursor, admin_list = self.db.page(self.entity_name, cursor=cursor, limit=limit, **kwargs)
        return new_cursor, [Admin.from_dict(admin_dict) for admin_dict in admin_list]


    def update(self, admin: Admin) -> Admin:
        return Admin.from_dict(self.db.update(self.entity_name, admin.to_dict()))


    def delete(self, admin_id: str) -> None:
        return self.db.delete(self.entity_name, admin_id)    
