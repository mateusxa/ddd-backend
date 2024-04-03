from infrastructure.storage.storage import Storage
from domain.entites.report import Report
from domain.repositories.report_repository import ReportRepository
from utils.error import InvalidAttribute, ObjectNotFound


class ReportService:

    repository: ReportRepository


    def __init__(self):
        self.repository = ReportRepository()


    def create(self, report: Report, local_path) -> Report:
        report_dict = self.repository.add(report.to_dict())
        report = Report.from_dict(report_dict)

        if not report.id:
            raise ObjectNotFound(f"Cannot save an report file with None id: {report}")
        
        if not local_path:
            raise InvalidAttribute(f"Cannot save an report file without a file(path/to/file): {report}")

        report = report.set(
            bucket_url=Storage.upload_file_to_folder(
                folder = self.repository.name,
                filename = report.id,
                file_path = local_path
            )
        )
        return Report.from_dict(self.repository.update(report.to_dict()))
    

    def delete(self, report_id: str) -> None:
        Storage.delete_file_from_folder(
            folder = self.repository.name,
            filename = report_id,
        )
        return self.repository.delete(report_id)
    

    def get_by_id(self, report_id: str):
        report_dict = self.repository.get_by_id(report_id)
        if report_dict:
            return Report.from_dict(report_dict)
        raise ObjectNotFound(f"No reports with {report_id}")
    

    def page(self, cursor: str | None = None, limit: int | None = None, company_id: str | None = None):
        new_cursor, reports_dict = self.repository.page(cursor=cursor, limit=limit, company_id=company_id)
        return new_cursor, [Report.from_dict(report) for report in reports_dict if report]
    