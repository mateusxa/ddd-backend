from random import randint
import uuid
from domain.entites.customer import Customer
from domain.services.customer_service import CustomerService


def test_create_customer():
    name = "name"
    email = "email"
    password = "password"
    company_id = str(uuid.uuid4())
    
    customer_service = CustomerService()

    customer = customer_service.create(
        Customer(
            company_id = company_id,
            name = name,
            email = email,
            password = password,
        )
    )

    assert customer.name == name
    assert customer.email == email
    assert customer.hashed_password != password


def test_create_and_update_customer():
    company_id = str(uuid.uuid4())
    customer_service = CustomerService()
    customer = customer_service.create(Customer(
        company_id=company_id,
        name="name",
        email="email",
        password="password",
    ))

    assert customer.id
    new_password = "new_password"
    new_customer = customer_service.update(customer_id=customer.id, password=new_password)

    assert new_customer.verify_password(new_password)


def test_page_customer():
    company_id = str(uuid.uuid4())
    customer_service = CustomerService()
    name = f"testting{randint(1111, 9999)}"

    for _ in range(6):
        customer_service.create(Customer(
            company_id=company_id,
            name=name,
            email="email",
            password="password",
        ))

    last_created = None
    while True:
        old_last_created = last_created
        last_created, document_list = customer_service.page(
            last_created=last_created,
            limit=2,
        )
        if not last_created:
            break

        if old_last_created:
            assert old_last_created != last_created
        # assert len(document_list) == 2

