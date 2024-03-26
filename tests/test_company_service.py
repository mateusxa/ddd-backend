import uuid
import pytest
from domain.entites.report import Report, ReportId
from domain.entites.company import Company
from domain.entites.customer import Customer
from domain.services.company_service import CompanyService
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


def test_create_and_get_company_by_name():
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

    got_companies = company_service.get_by_name(name=name)

    for got_company in got_companies:
        assert got_company.name == name


def test_page_company():
    company_service = CompanyService()

    for _ in range(6):
        company_service.create(Company(
            name = "TestCompany",
            tax_id = "31.899.356/0001-32",
        ))

    last_created = None
    while True:
        old_last_created = last_created
        last_created, document_list = company_service.page(
            last_created=last_created,
            limit=2,
        )
        if not last_created:
            break

        if old_last_created:
            assert old_last_created != last_created
        # assert len(document_list) == 2

