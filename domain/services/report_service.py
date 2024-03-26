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

        report.bucket_url = Storage.upload_file_to_folder(
            folder = report.get_class_name(),
            filename = report.id.value,
            file_path = local_path
        )
        return Report.from_dict(self.repository.update(report))
    

    def delete(self, report_id: ReportId) -> None:
        return self.repository.delete(report_id)
    

    def get_by_id(self, report_id: ReportId):
        report_dict = self.repository.get_by_id(report_id)
        if report_dict:
            return Report.from_dict(report_dict)
        raise Exception(f"No reports with {report_id}")
    