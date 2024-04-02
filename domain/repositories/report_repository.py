from datetime import datetime
from repository.reposity import Repository


class ReportRepository:

    name: str
    repository: Repository



    def __init__(self):
        self.name = "reports"
        self.repository = Repository()


    def save(self, admin_dict: dict) -> dict:
        return self.repository.save(self.name, admin_dict)
        

    def get_by_id(self, admin_id: str):
        return self.repository.get_by_id(self.name, admin_id)


    def get_by_fields(
        self, limit: int | None = None, created_before: datetime | None = None, 
        created_after: datetime | None = None, **kwargs
    ):
        return self.repository.get_by_fields(
            self.name, 
            limit=limit,
            created_before=created_before, 
            created_after=created_after, 
            **kwargs
        )    

        
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs):
        return self.repository.page(self.name, cursor=cursor, limit=limit, **kwargs)
    

    def update(self, dict_data: dict) -> dict:
        return self.repository.update(self.name, dict_data)


    def delete(self, obj_id: str) -> None:
        self.repository.delete(self.name, obj_id)