from datetime import datetime
from infrastructure.storage.storage import Storage
from repository.reposity import Repository
from domain.entites.report import Report, ReportId


class ReportService:

    repository: Repository


    def __init__(self):
        self.repository = Repository()


    def create(self, report: Report, local_path) -> Report:
        report_dict = self.repository.save(report)
        report = Report.from_dict(report_dict)

        if not report.id:
            raise Exception(f"Cannot save an report file with None id: {report}")
        
        if not local_path:
            raise Exception(f"Cannot save an report file without a file(path/to/file): {report}")

        report = report.set(
            bucket_url=Storage.upload_file_to_folder(
                folder = report.get_class_name(),
                filename = report.id.value,
                file_path = local_path
            )
        )
        return Report.from_dict(self.repository.update(report))
    

    def delete(self, report_id: ReportId) -> None:
        Storage.delete_file_from_folder(
            folder = report_id.get_class_name(),
            filename = report_id.value,
        )
        return self.repository.delete(report_id)
    

    def get_by_id(self, report_id: ReportId):
        report_dict = self.repository.get_by_id(report_id)
        if report_dict:
            return Report.from_dict(report_dict)
        raise Exception(f"No reports with {report_id}")
    

    def page(self, last_created: datetime | None = None, limit: int | None = None, company_id: str | None = None):
        return self.repository.page("reports", last_created=last_created, limit=limit, company_id=company_id)
    