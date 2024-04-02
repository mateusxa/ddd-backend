from domain.entites.company import Company
from domain.repositories.company_repository import CompanyRepository


class CompanyService:

    repository: CompanyRepository


    def __init__(self):
        self.repository = CompanyRepository()


    def create(self, company: Company) -> Company:
        company_dict = self.repository.save(company.to_dict())
        return Company.from_dict(company_dict)


    def delete(self, company_id: str) -> None:
        return self.repository.delete(company_id)

    def get_by_id(self, company_id: str):
        company_dict = self.repository.get_by_id(company_id)
        if company_dict:
            return Company.from_dict(company_dict)
        raise Exception(f"No companies with {company_id}")
    

    def get_by_name(self, name: str):
        return [Company.from_dict(company_dict) for company_dict in self.repository.get_by_fields(name=name)]
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        new_cursor, companies_dict = self.repository.page(cursor=cursor, limit=limit)
        return new_cursor, [Company.from_dict(company) for company in companies_dict if company]
