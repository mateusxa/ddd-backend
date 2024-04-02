import jwt
from os import environ
from datetime import datetime, timedelta, timezone
from domain.entites.admin import Admin
from infrastructure.email.email import EmailService
from domain.services.company_service import CompanyService
from domain.repositories.admin_repository import AdminRepository


class AdminService:

    repository: AdminRepository


    def __init__(self):
        self.repository = AdminRepository()


    def create(self, admin: Admin) -> Admin:
        admin_dict = self.repository.save(admin.to_dict())
        return Admin.from_dict(admin_dict)
    

    def delete(self, admin_id: str) -> None:
        return self.repository.delete(admin_id)
    

    def update(self, admin_id: str, password: str | None = None) -> Admin:
        admin = self.get_by_id(admin_id)
        return admin.set(password)
    

    def get_by_id(self, admin_id: str):
        admin_dict = self.repository.get_by_id(admin_id)
        if admin_dict:
            return Admin.from_dict(admin_dict)
        raise Exception(f"No admins with {admin_id}")
    

    def get_by_email(self, email: str):
        admin_list = [Admin.from_dict(admin_dict) for admin_dict in self.repository.get_by_fields(email=email)]
        return admin_list[0]
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        new_cursor, admins_dict = self.repository.page(cursor=cursor, limit=limit)
        return new_cursor, [Admin.from_dict(admin) for admin in admins_dict if admin] if admins_dict else []
    

    def get_token_by_email_and_password(self, email: str, password: str) -> str:
        admin = self.get_by_email(email)
        if not admin or not admin.id:
            raise Exception("Invalid email!")
        if not admin.is_password_valid(password):
            raise Exception("Invalid password!")
        token = jwt.encode({
            "id": admin.id
        }, environ['ADMIN_JWT_SECRET'])
        return token


    @staticmethod
    def get_id_by_token(token: str) -> str:
        payload = jwt.decode(token, environ['ADMIN_JWT_SECRET'], verify=True, algorithms=["HS256"])
        return payload['id']


    def invite_customer(self, customer_email: str, company_id: str):
        company = CompanyService().get_by_id(company_id)
        data = {
            'company_id': company_id,
            'expires_after': (datetime.now(timezone.utc) + timedelta(days=1)).timestamp(),
        }

        jwt_token = jwt.encode(data, environ["INVITE_JWT_SECRET"], algorithm='HS256')
        url = f"https://{environ['DOMAIN']}/invite/{jwt_token}" 

        with open('utils/invite_email_template.html', 'r', encoding='utf-8') as file:
            body = file.read().format(
                url=url,
                company_name=company.name,
            )
        EmailService.send_email(
            to_address=customer_email,
            subject=f"Convidado para {company.name}",
            body=body
        )
        return jwt_token
