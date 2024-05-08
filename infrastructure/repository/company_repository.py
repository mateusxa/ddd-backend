from datetime import datetime
from domain.entites.company import Company
from infrastructure.data_mapper.sqlalchemy.company import company_entity_to_model, company_model_to_entity
from infrastructure.firebase.firestore import Firestore
from infrastructure.models.sqlalchemy.company import CompanyModel
from infrastructure.repository import Repository
from utils.error import Error


class CompanyRepository(Repository):

    entity_name: str

    def __init__(self):
        super().__init__()
        self.entity_name = "companies"


    def create(self, company: Company) -> Company:
        instance = company_entity_to_model(company)
        self.session.add(instance)
        self.session.commit()
        return company_model_to_entity(instance)
        

    def get_by_id(self, company_id: str) -> Company | None:
        instance = self.session.get(CompanyModel, company_id)
        if not instance:
            return None
        return company_model_to_entity(instance)


    def get_by_name(self, name):
        instance = self.session.query(CompanyModel).filter_by(name=name).first()
        if not instance:
            return None
        return company_model_to_entity(instance)


    def get_by_tax_id(self, tax_id):
        instance = self.session.query(CompanyModel).filter_by(tax_id=tax_id).first()
        if not instance:
            return None
        return company_model_to_entity(instance)


    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Company]]:
        company_id = self.decode_cursor(cursor)
        instances = self.session.query(CompanyModel).filter_by(id=company_id).limit(limit).all()
        
        new_cursor = None
        company_list = []
        for instance in instances:
            company = company_model_to_entity(instance)
            company_list.append(company)
            if not company.id:
                raise Error(Error.Code.internal_error, "Mapped company without id", 500)
            new_cursor = company.id

        new_cursor = self.encode_cursor(new_cursor)
        return new_cursor,  company_list


    def update(self, company: Company) -> Company:
        if not company.id:
            # TODO fix error  
            raise Error("update", "update")
        
        instance = self.session.get(CompanyModel, company.id)
        if not instance:
            # TODO fix error
            raise Error("not exists", "object not exists")
        
        instance.name = company.name
        self.session.commit()
        return company_model_to_entity(instance)


    def delete(self, company_id: str) -> None:
        company_model = self.session.get(CompanyModel, company_id)
        self.session.delete(company_model)   
        self.session.commit()

    
    def __getitem__(self, key):
        return self.get_by_id(key)  
