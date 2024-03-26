from infrastructure.storage.storage import Storage
from repository.reposity import Repository
from domain.entites.admin import Admin
from domain.entites.report import Report, ReportId
from domain.entites.company import Company, CompanyId
from domain.entites.customer import Customer


class AdminService:

    repository: Repository


    def __init__(self):
        self.repository = Repository()


    def create(self, admin: Admin):
        admin_dict = self.repository.save(admin)
        return Admin.from_dict(admin_dict)

