from domain.entites.company import Company
from domain.repositories.company_repository import CompanyRepository
from utils.validateCNPJ import validate_cnpj
from utils.error import DuplicatedAttribute, DuplicatedEntities, InvalidAttribute, ObjectNotFound


class CompanyService:

    repository: CompanyRepository


    def __init__(self):
        self.repository = CompanyRepository()


    def create(self, company: Company) -> Company:
        tax_id = validate_cnpj(company.tax_id)
        if not tax_id:
            raise InvalidAttribute(f"CNPJ invalid {tax_id}")
        
        if self.get_by_tax_id(company.tax_id):
            raise DuplicatedAttribute(f"Company tax_id {company.tax_id} already exists!")

        if self.get_by_name(company.name):
            raise DuplicatedAttribute(f"Company name {company.name} already exists!")

        company_dict = self.repository.add(company.to_dict())
        return Company.from_dict(company_dict)


    def delete(self, company_id: str) -> None:
        return self.repository.delete(company_id)


    def get_by_id(self, company_id: str):
        company_dict = self.repository.get_by_id(company_id)
        if company_dict:
            return Company.from_dict(company_dict)
        raise ObjectNotFound(f"No companies with {company_id}")
    

    def get_by_name(self, name: str):
        company_dict = [Company.from_dict(company_dict) for company_dict in self.repository.get_by_fields(name=name)]
        if len(company_dict) > 1:
            raise DuplicatedEntities(f"More than 1 Company with same name: {name}")
        
        return company_dict[0] if len(company_dict) > 0 else None
    

    def get_by_tax_id(self, tax_id: str):
        company_dict = [Company.from_dict(company_dict) for company_dict in self.repository.get_by_fields(tax_id=tax_id)]
        if len(company_dict) > 1:
            raise DuplicatedEntities(f"More than 1 Company with same tax_id: {tax_id}")
        
        return company_dict[0] if len(company_dict) > 0 else None


    def page(self, cursor: str | None = None, limit: int | None = None):
        new_cursor, companies_dict = self.repository.page(cursor=cursor, limit=limit)
        return new_cursor, [Company.from_dict(company) for company in companies_dict if company]
