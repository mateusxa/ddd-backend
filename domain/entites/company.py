from datetime import datetime


class Company:
    
    name: str
    tax_id: str
    id: str | None
    created: datetime | None


    def __init__(self, name: str, tax_id: str, id: str | None = None, created: datetime | None = None):
        self.name = name
        self.tax_id = tax_id
        self.id = id
        self.created = created or datetime.now()


    @staticmethod
    def from_dict(dict: dict):
        if not all(attr in dict for attr in Company.__annotations__):
            raise Exception(f"dict incomplete! {dict}")
        return Company(
            name = dict["name"],
            tax_id = dict["tax_id"],
            id = dict["id"],
            created = dict["created"],
        )
