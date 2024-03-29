from random import randint

import pytest
from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


def test_create_and_get_admin():
    name = "name"
    email = "email"

    admin_service = AdminService()
    created_admin = admin_service.create(Admin(
        name=name,
        email=email,
        password="password",
    ))

    assert created_admin.id
    got_company = admin_service.get_by_id(created_admin.id)

    assert got_company.name == name
    assert got_company.email == email


def test_create_and_update_admin():
    admin_service = AdminService()
    admin = admin_service.create(Admin(
        name="name",
        email="email",
        password="password",
    ))

    assert admin.id
    new_password = "new_password"
    new_admin = admin_service.update(admin_id=admin.id, password=new_password)

    assert new_admin.is_password_valid(new_password)

def test_get_token_by_email_and_password_and_get_id_by_token():
    name = "name"
    email = "email"
    password = "password"
    
    admin_service = AdminService()
    admin = admin_service.create(Admin(
        name=name,
        email=email,
        password=password,
    ))
    token = admin_service.get_token_by_email_and_password(email=admin.email, password=password)

    assert token

    admin_id = AdminService.get_id_by_token(token)
    got_company = admin_service.get_by_id(admin_id)

    assert got_company.name == name
    assert got_company.email == email


def test_fail_get_token_by_email_and_password():
    name = "name"
    email = "email"
    
    admin_service = AdminService()
    admin = admin_service.create(Admin(
        name=name,
        email=email,
        password="password",
    ))

    with pytest.raises(Exception):
        admin_service.get_token_by_email_and_password(email=admin.email, password="wrong_password")


def test_page_admin():
    admin_service = AdminService()
    name = f"testting{randint(1111, 9999)}"

    for _ in range(6):
        admin_service.create(Admin(
            name=name,
            email="email",
            password="password",
        ))

    cursor = None
    while True:
        old_cursor = cursor
        cursor, document_list = admin_service.page(
            cursor=cursor,
            limit=2,
        )
        if not cursor:
            break

        if old_cursor:
            assert old_cursor != cursor
        # assert len(document_list) == 2
