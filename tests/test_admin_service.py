from random import randint
from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


def test_create_and_get_admin():
    admin_service = AdminService()
    admin_service.create(Admin(
        name="name",
        email="email",
        password="password",
    ))


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

    assert new_admin.verify_password(new_password)



def test_page_admin():
    admin_service = AdminService()
    name = f"testting{randint(1111, 9999)}"

    for _ in range(6):
        admin_service.create(Admin(
            name=name,
            email="email",
            password="password",
        ))

    last_created = None
    while True:
        old_last_created = last_created
        last_created, document_list = admin_service.page(
            last_created=last_created,
            limit=2,
        )
        if not last_created:
            break

        if old_last_created:
            assert old_last_created != last_created
        # assert len(document_list) == 2
