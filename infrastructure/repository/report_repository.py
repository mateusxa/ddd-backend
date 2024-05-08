from domain.entites.report import Report
from infrastructure.data_mapper.sqlalchemy.report import report_entity_to_model, report_model_to_entity
from infrastructure.models.sqlalchemy.report import ReportModel
from infrastructure.repository import Repository
from utils.error import Error


class ReportRepository(Repository):

    entity_name: str

    def __init__(self):
        super().__init__()
        self.entity_name = "reports"


    def create(self, report: Report) -> Report:
        instance = report_entity_to_model(report)
        self.session.add(instance)
        self.session.commit()
        return report_model_to_entity(instance)
        

    def get_by_id(self, report_id: str) -> Report | None:
        instance = self.session.get(ReportModel, report_id)
        if not instance:
            return None
        return report_model_to_entity(instance)

        
    def page(self, cursor: str | None = None, limit: int | None = None) -> tuple[str | None, list[Report]]:
        report_id = self.decode_cursor(cursor)
        instances = self.session.query(ReportModel).filter_by(id=report_id).limit(limit).all()
        
        new_cursor = None
        report_list = []
        for instance in instances:
            report = report_model_to_entity(instance)
            report_list.append(report)
            if not report.id:
                raise Error(Error.Code.internal_error, "Mapped report without id", 500)
            new_cursor = report.id

        new_cursor = self.encode_cursor(new_cursor)
        return new_cursor,  report_list


    def update(self, report: Report) -> Report:
        if not report.id:
            # TODO fix error  
            raise Error("update", "update")
        
        instance = self.session.get(ReportModel, report.id)
        if not instance:
            # TODO fix error
            raise Error("not exists", "object not exists")
        
        instance.name = report.name
        instance.bucket_url = report.bucket_url
        self.session.commit()
        return report_model_to_entity(instance)


    def delete(self, report_id: str) -> None:
        report_model = self.session.get(ReportModel, report_id)
        self.session.delete(report_model)   
        self.session.commit()

    
    def __getitem__(self, key):
        return self.get_by_id(key)
    