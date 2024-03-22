from domain.entites.admin import Admin


def test_hash_password():
    name = "name"
    email = "email"
    password = "password"
    
    admin = Admin(
        name = name,
        email = email,
        password = password,
    )

    assert admin.name == name
    assert admin.email == email
    assert admin.hased_password != password

def test_verify_password():
    name = "name"
    email = "email"
    password = "password"
    
    admin = Admin(
        name = name,
        email = email,
        password = password,
    )

    assert admin.hased_password != password
    assert admin.verify_password(password)
