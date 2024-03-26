from datetime import datetime
from infrastructure.storage.storage import Storage
from repository.reposity import Repository
from domain.entites.admin import Admin, AdminId
from domain.entites.report import Report, ReportId
from domain.entites.company import Company, CompanyId
from domain.entites.customer import Customer


class AdminService:

    repository: Repository


    def __init__(self):
        self.repository = Repository()


    def create(self, admin: Admin) -> Admin:
        admin_dict = self.repository.save(admin)
        return Admin.from_dict(admin_dict)
    

    def get_by_id(self, admin_id: AdminId):
        admin_dict = self.repository.get_by_id(admin_id)
        if admin_dict:
            return Admin.from_dict(admin_dict)
        raise Exception(f"No admins with {admin_id}")
    

    def update(self, admin_id: AdminId, password: str | None = None) -> Admin:
        admin = self.get_by_id(admin_id)
        return admin.set(password)
    

    def page(self, last_created: datetime | None = None, limit: int | None = None):
        return self.repository.page("repositories", last_created=last_created, limit=limit)
