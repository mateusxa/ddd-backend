import jwt
from os import environ
from datetime import datetime, timedelta, timezone
from infrastructure.email.email import EmailService
from domain.entites.admin import Admin
from domain.services.company_service import CompanyService
from domain.repositories.admin_repository import AdminRepository
from utils.error import Error


class AdminService:

    repository: AdminRepository

    def __init__(self):
        self.repository = AdminRepository()


    def create(self, admin: Admin) -> Admin:
        if self.get_by_email(admin.email):
            raise Error(Error.Code.invalid_attribute, f"Admin email already exists!", 400)
        return self.repository.create(admin)
    

    def update(self, admin_id: str, password: str | None = None) -> Admin:
        admin = self.get_by_id(admin_id)
        if not admin:
            raise Error(Error.Code.object_not_found, f"No admin with id: {admin_id}!", 400)
        if password:
            admin.hashed_password = password
        return self.repository.update(admin)
    
    
    def delete(self, admin_id: str) -> None:
        return self.repository.delete(admin_id)


    def get_by_id(self, admin_id: str) -> Admin | None:
        return self.repository.get_by_id(admin_id)
    

    def get_by_email(self, email: str) -> Admin | None:
        admin_list = self.repository.get_by_fields(email=email)
        if len(admin_list) > 1:
            raise Error(Error.Code.internal_error, f"More than 1 Admin with same email: {email}", 500)
        return admin_list[0] if len(admin_list) > 0 else None
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        return self.repository.page(cursor=cursor, limit=limit)
    

    def get_token_by_email_and_password(self, email: str, password: str) -> str:
        admin = self.get_by_email(email)
        if not admin or not admin.id:
            raise Error(Error.Code.invalid_attribute, f"Invalid email!", 400)
        if not admin.is_password_valid(password):
            raise Error(Error.Code.invalid_attribute, f"Invalid password!", 400)
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
        if not company:
            raise Error(Error.Code.object_not_found, f"No company with id: {company_id}!", 400)
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
