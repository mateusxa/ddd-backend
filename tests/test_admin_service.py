from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


def test_create_and_get_company():
    admin_service = AdminService()
    admin_service.create(Admin(
        name="name",
        email="email",
        password="password",
    ))

