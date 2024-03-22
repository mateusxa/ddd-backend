from logging import warning
import uuid
from domain.entites.customer import Customer
from domain.entites.company import Company
from domain.entites.report import Report
from domain.services.admin_service import AdminService
from domain.services.customer_service import CustomerService
from tests import ADMIN, ADMIN_PASSWORD


ADMIN.verify_password(ADMIN_PASSWORD)
admin_service = AdminService(ADMIN)

company_id = str(uuid.uuid4())
name = "name"
email = "email"
password = "password"

customer = admin_service.create_customer(
    Customer(
        company_id = company_id,
        name = name,
        email = email,
        password = password,
    )
)


def test_get_reports():
    name = "TestCompany"

    ADMIN.verify_password(ADMIN_PASSWORD)
    admin_service = AdminService(ADMIN)

    with open('/home/mateus/projects/xpaEnghenharia/tests/image.jpeg', 'rb') as f:
        report_blob = f.read()
        report = admin_service.create_report(
            Report(
                company_id = company_id,
                name = name,
                data = report_blob
            )
        )

    customer_service = CustomerService(customer)
    for report in customer_service.get_reports():
        assert report.id != None
        assert report.company_id == company_id


