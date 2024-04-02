import os
import uuid
import pytest
from random import randint
from dotenv import load_dotenv
from domain.entites.customer import Customer
from domain.services.admin_service import AdminService
from domain.services.company_service import CompanyService
from domain.services.customer_service import CustomerService


load_dotenv()


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

    assert new_customer.is_password_valid(new_password)

def test_get_token_by_email_and_password_and_get_id_by_token():
    name = "name"
    email = "email"
    password = "password"
    company_id = str(uuid.uuid4())
    
    customer_service = CustomerService()
    customer = customer_service.create(Customer(
        company_id=company_id,
        name=name,
        email=email,
        password=password,
    ))
    token = customer_service.get_token_by_email_and_password(email=customer.email, password=password)

    assert token

    customer_id, company_id = CustomerService.get_id_and_company_id_by_token(token)
    got_customer = customer_service.get_by_id(customer_id)

    assert got_customer.name == name
    assert got_customer.company_id == company_id
    assert got_customer.email == email


def test_fail_get_token_by_email_and_password():
    name = "name"
    email = "email"
    company_id = str(uuid.uuid4())
    
    customer_service = CustomerService()
    customer = customer_service.create(Customer(
        company_id=company_id,
        name=name,
        email=email,
        password="password",
    ))

    with pytest.raises(Exception):
        customer_service.get_token_by_email_and_password(email=customer.email, password="wrong_password")

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

    cursor = None
    while True:
        old_cursor = cursor
        cursor, document_list = customer_service.page(
            cursor=cursor,
            limit=2,
        )
        if not cursor:
            break

        if old_cursor:
            assert old_cursor != cursor
        # assert len(document_list) == 2
            
def test_create_with_token():
    company_service = CompanyService()
    company = company_service.get_by_name("TestCompany")[0]
    assert company.id
    admin_service = AdminService()
    token = admin_service.invite_customer(os.environ["TARGET_EMAIL"], company_id=company.id)


    name = "name"
    email = "email"
    password = "password"
    custome_service = CustomerService()
    customer = custome_service.create_with_token(
        token=token,
        name=name,
        email=email,
        password=password,
    )

    assert customer.company_id == company.id
    assert customer.name == name
    assert customer.email == email
    assert customer.hashed_password != password
