import uuid
import pytest
from domain.entites.report import Report, ReportId
from domain.entites.company import Company
from domain.entites.customer import Customer
from domain.services.admin_service import AdminService
from domain.services.company_service import CompanyService


def test_create_and_get_company():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"

    company = Company(
        name = name,
        tax_id = tax_id,
    )
    company_service = CompanyService()
    company = company_service.create(company)

    assert company.id != None
    assert company.name == name
    assert company.tax_id == tax_id

    got_company = company_service.get_by_id(company.id)

    assert got_company.name == name
    assert got_company.tax_id == tax_id
