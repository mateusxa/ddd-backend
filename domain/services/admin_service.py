import os
import jwt
from datetime import datetime, timedelta, timezone
from repository.reposity import Repository
from infrastructure.email.email import EmailService
from domain.entites.company import CompanyId
from domain.entites.admin import Admin, AdminId
from domain.services.company_service import CompanyService


class AdminService:

    repository: Repository


    def __init__(self):
        self.repository = Repository()


    def create(self, admin: Admin) -> Admin:
        admin_dict = self.repository.save(admin)
        return Admin.from_dict(admin_dict)
    

    def get_by_id(self, admin_id: AdminId):
        admin_dict = self.repository.get_by_id(admin_id)
        if admin_dict:
            return Admin.from_dict(admin_dict)
        raise Exception(f"No admins with {admin_id}")
    

    def update(self, admin_id: AdminId, password: str | None = None) -> Admin:
        admin = self.get_by_id(admin_id)
        return admin.set(password)
    

    def page(self, last_created: datetime | None = None, limit: int | None = None):
        return self.repository.page("repositories", last_created=last_created, limit=limit)
    

    def invite_customer(self, customer_email: str, company_id: CompanyId):
        company = CompanyService().get_by_id(company_id)
        data = {
            'company_id': company_id.value,
            'expires_after': (datetime.now(timezone.utc) + timedelta(days=1)).timestamp(),
        }

        jwt_token = jwt.encode(data, os.environ["JWT_SECRET"], algorithm='HS256')
        url = f"https://{os.environ['DOMAIN']}/invite/{jwt_token}" 

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
