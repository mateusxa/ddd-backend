import uuid
from tests import ADMIN, ADMIN_PASSWORD
from domain.entites.report import Report
from domain.entites.company import Company
from domain.entites.customer import Customer
from domain.services.admin_service import AdminService


def test_create_and_get_company():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"

    ADMIN.verify_password(ADMIN_PASSWORD)
    admin_service = AdminService(ADMIN)

    company = Company(
        name = name,
        tax_id = tax_id,
    )
    company = admin_service.create_company(company)

    assert company.id != None
    assert company.name == name
    assert company.tax_id == tax_id

    got_company = admin_service.get_company(company.id)

    assert got_company.name == name
    assert got_company.tax_id == tax_id


def test_create_and_get_report():
    name = "TestCompany"
    company_id = str(uuid.uuid4())

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

    assert report.id != None
    assert report.name == name
    assert report.company_id == company_id

    got_report = admin_service.get_report(report.id)

    assert got_report.name == name
    assert got_report.company_id == company_id


def test_delete_and_get_report():
    name = "TestCompany"
    company_id = str(uuid.uuid4())

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

    if not report.id:
        raise Exception(f"report with empty id")
    
    deleted_report = admin_service.delete_report(report.id)

    assert deleted_report is None

    try:
        admin_service.get_report(report.id)
    except Exception as e:
        assert e


def test_create_customer():
    name = "name"
    email = "email"
    password = "password"
    company_id = str(uuid.uuid4())

    ADMIN.verify_password(ADMIN_PASSWORD)
    admin_service = AdminService(ADMIN)

    customer = admin_service.create_customer(
        Customer(
            company_id = company_id,
            name = name,
            email = email,
            password = password,
        )
    )

    assert customer.name == name
    assert customer.email == email
    assert customer.hased_password != password
