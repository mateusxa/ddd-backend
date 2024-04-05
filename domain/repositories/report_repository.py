from domain.entites.report import Report
from repository.reposity import Repository
from infrastructure.firebase.firestore import Firestore


class ReportRepository(Repository):

    entity_name: str

    def __init__(self):
        self.entity_name = "reports"
        self.db = Firestore()


    def create(self, report: Report) -> Report:
        return Report.from_dict(self.db.create(self.entity_name, report.to_dict()))
        

    def get_by_id(self, report_id: str) -> Report | None:
        report_dict = self.db.get_by_id(self.entity_name, report_id)
        return Report.from_dict(report_dict) if report_dict else None


    def get_by_fields(self, limit: int | None = None, **kwargs) -> list[Report]:
        return [Report.from_dict(report_dict) for report_dict in self.db.get_by_fields(self.entity_name, limit=limit, **kwargs)]

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs) -> tuple[str | None, list[Report]]:
        new_cursor, report_list = self.db.page(self.entity_name, cursor=cursor, limit=limit, **kwargs)
        return new_cursor, [Report.from_dict(report_dict) for report_dict in report_list]


    def update(self, report: Report) -> Report:
        return Report.from_dict(self.db.update(self.entity_name, report.to_dict()))


    def delete(self, report_id: str) -> None:
        return self.db.delete(self.entity_name, report_id)    
