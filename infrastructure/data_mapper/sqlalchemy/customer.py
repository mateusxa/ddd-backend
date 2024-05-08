from domain.entites.customer import Customer
from infrastructure.models.sqlalchemy.customer import CustomerModel


def customer_model_to_entity(instance) -> Customer:
    return Customer(
        id=str(instance.id),
        company_id=str(instance.company_id),
        name=instance.name,
        email=instance.email,
        password=instance.password,
        created=instance.created,
    )

def customer_entity_to_model(customer: Customer) -> CustomerModel:
    return CustomerModel(
        id=customer.id,
        company_id=customer.company_id,
        name=customer.name,
        email=customer.email,
        password=customer.password,
        created=customer.created,
    )