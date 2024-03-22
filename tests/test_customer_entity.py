from domain.entites.customer import Customer


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

    assert customer.name == name
    assert customer.email == email
    assert customer.hased_password != password


def test_verify_password():
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

    assert customer.hased_password != password
    assert customer.verify_password(password)
