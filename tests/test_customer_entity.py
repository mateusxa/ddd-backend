import pytest
from domain.entites.customer import Customer



def test_customer_id():
    id = "fake_id"
    customer_id = id

    assert customer_id == id
    assert str(customer_id) == id


def test_repr():
    company_id = "company_id"
    name = "name"
    email = "email"
    password = "password"

    customer = Customer(company_id, name, email, password=password)
    hashed_password = customer.hashed_password

    customer_string = f"Customer(\
            company_id={company_id}, \
            name={name}, \
            email={email}, \
            hashed_password={hashed_password}, \
            id={customer.id}, \
            created={customer.created}\
        )"
    
    assert customer_string == repr(customer)


def test_to_dict():
    company_id = "company_id"
    name = "name"
    email = "email"
    password = "password"
    
    customer_dict = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    ).to_dict()

    assert "company_id" in customer_dict
    assert "name" in customer_dict
    assert "email" in customer_dict
    assert "hashed_password" in customer_dict
    assert "id" in customer_dict
    assert "created" in customer_dict


def test_from_dict():
    company_id = "company_id"
    name = "name"
    email = "email"
    password = "password"

    customer = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )
    
    customer_dict = {
        "company_id": "company_id",
        "name": name,
        "email": email,
        "hashed_password": customer.hashed_password,
        "id": "",
        "created": customer.created,
    }

    new_customer = Customer.from_dict(customer_dict)

    assert new_customer.company_id == customer.company_id
    assert new_customer.name == customer.name
    assert new_customer.email == customer.email
    assert new_customer.hashed_password == customer.hashed_password
    assert str(new_customer.id) == ""
    assert new_customer.created == customer.created


def test_from_dict_fail():
    company_id = "company_id"
    name = "name"
    email = "email"
    password = "password"

    customer = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )
    
    customer_dict = {
        "company_id": company_id,
        "name": name,
        "hashed_password": customer.hashed_password,
        "id": "",
        "created": customer.created,
    }

    with pytest.raises(Exception):
        Customer.from_dict(customer_dict)


def test_hash_password():
    company_id = "id"
    name = "name"
    email = "email"
    password = "password"
    
    customer = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )

    assert customer.company_id == company_id
    assert customer.name == name
    assert customer.email == email
    assert customer.hashed_password != password


def test_is_password_valid():
    company_id = "id"
    name = "name"
    email = "email"
    password = "password"
    
    customer = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )

    assert customer.hashed_password != password
    assert customer.is_password_valid(password)


def test_is_password_valid_fail():
    company_id = "id"
    name = "name"
    email = "email"
    password = "password"
    
    customer = Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )

    assert not customer.is_password_valid("wrong_password")
