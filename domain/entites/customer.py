import hashlib
from datetime import datetime, timezone
from domain.entites.entity import Entity, EntityId
from utils.constants import SALT


class CustomerId(EntityId):

    def __init__(self, value: str):
        super().__init__(value)


class Customer(Entity):

    company_id: str
    name: str
    email: str
    hashed_password: str | None
    id: CustomerId | None
    created: datetime


    def __init__(
            self, company_id: str, name: str, email: str, password: str | None = None, hashed_password: str | None = None, 
            id: CustomerId | None = None, created: datetime | None = None
        ):
        self.company_id = company_id
        self.name = name
        self.email = email
        self.id = id
        self.hashed_password = self.__hash_password(password) if password else hashed_password
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
            raise Exception(f"dict incomplete! {source}")
        return Customer(
            id = CustomerId(source["id"]),
            company_id = source["company_id"],
            name = source["name"],
            email = source["email"],
            hashed_password = source["hashed_password"],
            created = source["created"],
        )
    

    def set(self, password: str | None = None):
        if password:
            self.hashed_password = Customer.__hash_password(password)
        return self

    def verify_password(self, password: str):
        if self.__hash_password(password) ==  self.hashed_password:
            self.verified = True
            return True
        return False
    
    def is_password_valid(self, password: str):
        if self.__hash_password(password) ==  self.hashed_password:
            self.verified = True
            return True
        return False
    
    @staticmethod
    def __hash_password(password: str) -> str:
        salted_password = f"{password}:{SALT}".encode('utf-8')
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(salted_password)        
        return hash_algorithm.hexdigest()
    