import pytest
from domain.entites.admin import Admin, AdminId


def test_admin_id():
    id = "fake_id"
    admin_id = AdminId(id)

    assert admin_id.id == id
    assert str(admin_id) == id


def test_repr():
    name = "name"
    email = "email"
    password = "password"

    admin = Admin(name, email, password=password)
    hashed_password = admin.hashed_password

    admin_string = f"Admin(\
            name={name}, \
            email={email}, \
            hashed_password={hashed_password}, \
            id={admin.id}, \
            created={admin.created}\
        )"
    
    assert admin_string == repr(admin)


def test_to_dict():
    name = "name"
    email = "email"
    password = "password"
    
    admin_dict = Admin(
        name = name,
        email = email,
        password = password,
    ).to_dict()

    assert "name" in admin_dict
    assert "email" in admin_dict
    assert "hashed_password" in admin_dict
    assert "id" in admin_dict
    assert "created" in admin_dict


def test_from_dict():
    name = "name"
    email = "email"
    password = "password"

    admin = Admin(
        name = name,
        email = email,
        password = password,
    )
    
    admin_dict = {
        "name": name,
        "email": email,
        "hashed_password": admin.hashed_password,
        "id": "",
        "created": admin.created,
    }

    new_admin = Admin.from_dict(admin_dict)

    assert new_admin.name == admin.name
    assert new_admin.email == admin.email
    assert new_admin.hashed_password == admin.hashed_password
    assert str(new_admin.id) == ""
    assert new_admin.created == admin.created


def test_from_dict_fail():
    name = "name"
    email = "email"
    password = "password"

    admin = Admin(
        name = name,
        email = email,
        password = password,
    )
    
    admin_dict = {
        "name": name,
        "hashed_password": admin.hashed_password,
        "id": "",
        "created": admin.created,
    }

    with pytest.raises(Exception):
        Admin.from_dict(admin_dict)


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
    assert admin.hashed_password != password


def test_verify_password():
    name = "name"
    email = "email"
    password = "password"
    
    admin = Admin(
        name = name,
        email = email,
        password = password,
    )

    assert admin.hashed_password != password
    assert admin.verify_password(password)


def test_verify_password_fail():
    name = "name"
    email = "email"
    password = "password"
    
    admin = Admin(
        name = name,
        email = email,
        password = password,
    )

    assert not admin.verify_password("wrong_pasword")