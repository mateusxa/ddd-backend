from domain.entites.company import Company
from infrastructure.models.sqlalchemy.company import CompanyModel


def company_model_to_entity(instance) -> Company:
    return Company(
        id=str(instance.id),
        name=instance.name,
        tax_id=instance.tax_id,
        created=instance.created,
    )

def company_entity_to_model(company: Company) -> CompanyModel:
    return CompanyModel(
        id=company.id,
        name=company.name,
        tax_id=company.tax_id,
        created=company.created,
    )