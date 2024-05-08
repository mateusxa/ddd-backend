from domain.entites.report import Report
from infrastructure.models.sqlalchemy.report import ReportModel


def report_model_to_entity(instance) -> Report:
    return Report(
        id=str(instance.id),
        company_id=str(instance.company_id),
        name=instance.name,
        bucket_url=instance.bucket_url,
        created=instance.created,
    )

def report_entity_to_model(report: Report) -> ReportModel:
    return ReportModel(
        id=report.id,
        company_id=report.company_id,
        name=report.name,
        bucket_url=report.bucket_url,
        created=report.created,
    )