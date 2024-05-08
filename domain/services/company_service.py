from infrastructure.repository.company_repository import CompanyRepository
from utils.error import Error
from utils.validateCNPJ import validate_cnpj
from domain.entites.company import Company


class CompanyService:

    repository: CompanyRepository

    def __init__(self):
        self.repository = CompanyRepository()


    def create(self, company: Company) -> Company:
        tax_id = validate_cnpj(company.tax_id)
        if not tax_id:
            raise Error(Error.Code.invalid_attribute, f"CNPJ invalid {tax_id}", 400)
        
        if self.get_by_tax_id(company.tax_id):
            raise Error(Error.Code.invalid_attribute, f"Company tax_id {company.tax_id} already exists!", 400)

        if self.get_by_name(company.name):
            raise Error(Error.Code.invalid_attribute, f"Company name {company.name} already exists!", 400)

        return self.repository.create(company)


    def delete(self, company_id: str) -> None:
        return self.repository.delete(company_id)


    def get_by_id(self, company_id: str) -> Company | None:
        return self.repository.get_by_id(company_id)
    

    def get_by_name(self, name: str):
        company_list = self.repository.get_by_fields(name=name)
        if len(company_list) > 1:
            raise Error(Error.Code.internal_error, f"More than 1 Company with same name: {name}", 500)
        return company_list[0] if len(company_list) > 0 else None
    

    def get_by_tax_id(self, tax_id: str):
        company_list = self.repository.get_by_fields(tax_id=tax_id)
        if len(company_list) > 1:
            raise Error(Error.Code.internal_error, f"More than 1 Company with same tax_id: {tax_id}", 500)
        return company_list[0] if len(company_list) > 0 else None


    def page(self, cursor: str | None = None, limit: int | None = None):
        return self.repository.page(cursor=cursor, limit=limit)
