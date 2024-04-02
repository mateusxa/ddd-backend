from domain.entites.company import Company
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

    cursor = None
    while True:
        old_cursor = cursor
        cursor, document_list = company_service.page(
            cursor=cursor,
            limit=2,
        )
        if not cursor:
            break

        if old_cursor:
            assert old_cursor != cursor
        # assert len(document_list) == 2

