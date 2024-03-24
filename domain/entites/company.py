from datetime import datetime

class CompanyId:

    id: str

    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


class Company:
    
    name: str
    tax_id: str
    id: CompanyId | None
    created: datetime | None


    def __init__(self, name: str, tax_id: str, id: CompanyId | None = None, created: datetime | None = None):
        self.name = name
        self.tax_id = tax_id
        self.id = id
        self.created = created or datetime.now()


    def __repr__(self):
        return f"Company(\
            name={self.name}, \
            tax_id={self.tax_id}, \
            id={self.id}, \
            created={self.created}\
        )"


    def to_dict(self):
        return vars(self)


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Company.__annotations__):
            raise Exception(f"dict incomplete! {source}")
        return Company(
            name = source["name"],
            tax_id = source["tax_id"],
            id = CompanyId(source["id"]),
            created = source["created"],
        )
