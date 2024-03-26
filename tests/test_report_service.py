import uuid
import pytest
from domain.entites.report import Report, ReportId
from domain.entites.company import Company
from domain.entites.customer import Customer
from domain.services.admin_service import AdminService
from domain.services.report_service import ReportService


def test_create_and_get_report():
    name = "TestCompany"
    company_id = str(uuid.uuid4())

    report = Report(
        company_id = company_id,
        name = name,
    )
    report_service = ReportService()
    report = report_service.create(report = report, local_path = "tests/file.pdf")

    assert report.id != None
    assert report.bucket_url != None
    assert report.name == name
    assert report.company_id == company_id

    got_report = report_service.get_by_id(report.id)

    assert got_report.name == name
    assert got_report.company_id == company_id


def test_get_report_fail():
    report_service = ReportService()

    with pytest.raises(Exception):
        report_service.get_by_id(ReportId("wrong_id"))


def test_delete_and_get_report():
    name = "TestCompany"
    company_id = str(uuid.uuid4())

    report = Report(
        company_id = company_id,
        name = name,
    )
    report_service = ReportService()
    report = report_service.create(report = report, local_path = "tests/file.pdf")

    if not report.id:
        raise Exception(f"report with empty id")
    
    deleted_report = report_service.delete(report.id)

    assert deleted_report is None

    with pytest.raises(Exception):
        report_service.get_by_id(report.id)
