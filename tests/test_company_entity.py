import pytest
from domain.entites.company import Company, CompanyId


def test_company_id():
    id = "fake_id"
    company_id = CompanyId(id)

    assert company_id.id == id
    assert str(company_id) == id


def test_repr():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"

    company = Company(name, tax_id)

    company_string = f"Company(\
            name={company.name}, \
            tax_id={company.tax_id}, \
            id={company.id}, \
            created={company.created}\
        )"
    
    assert company_string == repr(company)


def test_to_dict():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"
    
    company_dict = Company(name, tax_id).to_dict()

    assert "name" in company_dict
    assert "tax_id" in company_dict
    assert "id" in company_dict
    assert "created" in company_dict


def test_from_dict():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"
    
    company = Company(name, tax_id)
    
    company_dict = {
        "name": name,
        "tax_id": tax_id,
        "id": "",
        "created": company.created,
    }

    new_company = Company.from_dict(company_dict)

    assert new_company.name == company.name
    assert new_company.tax_id == company.tax_id
    assert str(new_company.id) == ""
    assert new_company.created == company.created


def test_from_dict_fail():
    name = "TestCompany"
    tax_id = "31.899.356/0001-32"
    
    company = Company(name, tax_id)
    
    company_dict = {
        "name": name,
        "id": "",
        "created": company.created,
    }

    with pytest.raises(Exception):
        Company.from_dict(company_dict)
