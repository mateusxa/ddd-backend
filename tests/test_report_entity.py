import uuid

import pytest
from domain.entites.report import Report, ReportId


def test_report_id():
    id = "fake_id"
    report_id = ReportId(id)

    assert report_id.id == id
    assert str(report_id) == id


def test_repr():
    name = "TestReport"
    company_id = str(uuid.uuid4())

    report = Report(company_id, name)

    report_string = f"Report(\
            company_id={report.company_id}, \
            name={report.name}, \
            data={report.data}, \
            bucket_url={report.bucket_url}, \
            id={report.id}, \
            created={report.created}\
        )"
    
    assert report_string == repr(report)


def test_to_dict():
    name = "TestReport"
    company_id = str(uuid.uuid4())
    
    report_dict = Report(company_id, name).to_dict()

    assert "company_id" in report_dict
    assert "name" in report_dict
    assert "bucket_url" in report_dict
    assert "id" in report_dict
    assert "created" in report_dict


def test_from_dict():
    name = "TestReport"
    company_id = str(uuid.uuid4())
    
    report = Report(company_id, name)
    
    report_dict = {
        "name": name,
        "company_id": company_id,
        "id": "",
        "bucket_url": "",
        "created": report.created,
    }

    new_report = Report.from_dict(report_dict)

    assert new_report.name == report.name
    assert new_report.company_id == report.company_id
    assert str(new_report.id) == ""
    assert new_report.created == report.created


def test_from_dict_fail():
    name = "TestReport"
    company_id = str(uuid.uuid4())
    
    report = Report(company_id, name)
    
    report_dict = {
        "name": name,
        "company_id": company_id,
        "created": report.created,
    }

    with pytest.raises(Exception):
        Report.from_dict(report_dict)
