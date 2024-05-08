from domain.entites.admin import Admin
from infrastructure.models.sqlalchemy.admin import AdminModel


def admin_model_to_entity(instance) -> Admin:
    return Admin(
        id=str(instance.id),
        name=instance.name,
        email=instance.email,
        password=instance.password,
        created=instance.created,
    )

def admin_entity_to_model(admin: Admin) -> AdminModel:
    return AdminModel(
        id=admin.id,
        name=admin.name,
        email=admin.email,
        password=admin.password,
        created=admin.created,
    )