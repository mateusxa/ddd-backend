from datetime import datetime, timezone
from domain.entites import UserEntity
from utils.error import DictIncomplete



class Customer(UserEntity):

    company_id: str
    name: str
    email: str
    hashed_password: str | None
    id: str | None
    created: datetime


    def __init__(
            self, company_id: str, name: str, email: str, password: str | None = None, hashed_password: str | None = None, 
            id: str | None = None, created: datetime | None = None
        ):
        self.company_id = company_id
        self.name = name
        self.email = email
        self.id = id
        self.hashed_password = self.hash_password(password) if password else hashed_password
        self.created = created or datetime.now(timezone.utc)

    def __repr__(self):
        return f"Customer(\
            company_id={self.company_id}, \
            name={self.name}, \
            email={self.email}, \
            hashed_password={self.hashed_password}, \
            id={self.id}, \
            created={self.created}\
        )"


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Customer.__annotations__):
            raise DictIncomplete(source)
        return Customer(
            id = source["id"],
            company_id = source["company_id"],
            name = source["name"],
            email = source["email"],
            hashed_password = source["hashed_password"],
            created = source["created"],
        )
    

    def set(self, password: str | None = None):
        if password:
            self.hashed_password = Customer.hash_password(password)
        return self
    