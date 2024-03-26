from repository.reposity import Repository
from domain.entites.company import Company, CompanyId


class CompanyService:

    repository: Repository


    def __init__(self):
        self.repository = Repository()


    def create(self, company: Company) -> Company:
        company_dict = self.repository.save(company)
        return Company.from_dict(company_dict)


    def get_by_id(self, company_id: CompanyId):
        company_dict = self.repository.get_by_id(company_id)
        if company_dict:
            return Company.from_dict(company_dict)
        raise Exception(f"No companies with {company_id}")
    
