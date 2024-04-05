from utils.error import Error
from infrastructure.storage.storage import Storage
from domain.entites.report import Report
from domain.repositories.report_repository import ReportRepository


class ReportService:

    repository: ReportRepository


    def __init__(self):
        self.repository = ReportRepository()


    def create(self, report: Report, local_path) -> Report:
        if not local_path:
            raise Error(Error.Code.invalid_attribute, f"Cannot save an report file without a file(path/to/file): {report}", 400)
        
        report = self.repository.create(report)
        if not report.id:
            raise Error(Error.Code.internal_error, f"Cannot save an report file with None id: {report}", 500)
        
        report.bucket_url = Storage.upload_file_to_folder(
            folder = self.repository.entity_name,
            filename = report.id,
            file_path = local_path
        )
        return self.repository.update(report)
    

    def delete(self, report_id: str) -> None:
        Storage.delete_file_from_folder(
            folder = self.repository.entity_name,
            filename = report_id,
        )
        return self.repository.delete(report_id)
    

    def get_by_id(self, report_id: str) -> Report | None:
        return self.repository.get_by_id(report_id)
    

    def page(self, cursor: str | None = None, limit: int | None = None):
        return self.repository.page(cursor=cursor, limit=limit)
    