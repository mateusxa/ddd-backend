from domain.entites.admin import Admin
from domain.services.admin_service import AdminService


ADMIN_PASSWORD = "password"

ADMIN = AdminService(
    Admin(
        name="name",
        email="email",
        password=ADMIN_PASSWORD,
    )
).create_admin()