from datetime import datetime
from domain.entites.company import Company
from infrastructure.firebase.firestore import Firestore
from repository.reposity import Repository


class CompanyRepository(Repository):

    entity_name: str

    def __init__(self):
        self.entity_name = "companies"
        self.db = Firestore()


    def create(self, company: Company) -> Company:
        return Company.from_dict(self.db.create(self.entity_name, company.to_dict()))
        

    def get_by_id(self, company_id: str) -> Company | None:
        company_dict = self.db.get_by_id(self.entity_name, company_id)
        return Company.from_dict(company_dict) if company_dict else None


    def get_by_fields(self, limit: int | None = None, **kwargs) -> list[Company]:
        return [Company.from_dict(company_dict) for company_dict in self.db.get_by_fields(self.entity_name, limit=limit, **kwargs)]

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Company]]:
        new_cursor, company_list = self.db.page(self.entity_name, cursor=cursor, limit=limit, **kwargs)
        return new_cursor, [Company.from_dict(company_dict) for company_dict in company_list]


    def update(self, company: Company) -> Company:
        return Company.from_dict(self.db.update(self.entity_name, company.to_dict()))


    def delete(self, company_id: str) -> None:
        return self.db.delete(self.entity_name, company_id)    
