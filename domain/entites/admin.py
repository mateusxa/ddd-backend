import hashlib
from datetime import datetime, timezone
from utils.constants import SALT
from domain.entites.entity import Entity, EntityId


class AdminId(EntityId):

    def __init__(self, value: str):
        super().__init__(value)


class Admin(Entity):
    
    name: str
    email: str
    hashed_password: str | None
    id: AdminId | None
    created: datetime


    def __init__(
            self, name: str, email: str, password: str | None = None, hashed_password: str | None = None, 
            id: AdminId | None = None, created: datetime | None = None
        ):
        self.name = name
        self.email = email
        self.hashed_password = self.__hash_password(password) if password else hashed_password
        self.id = id
        self.created = created or datetime.now(timezone.utc)


    def __repr__(self):
        return f"Admin(\
            name={self.name}, \
            email={self.email}, \
            hashed_password={self.hashed_password}, \
            id={self.id}, \
            created={self.created}\
        )"
    

    def set(self, password: str | None = None):
        if password:
            self.hashed_password = Admin.__hash_password(password)
        return self


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Admin.__annotations__):
            raise Exception(f"dict incomplete! {source}")
        return Admin(
            id = AdminId(source["id"]),
            name = source["name"],
            email = source["email"],
            hashed_password = source["hashed_password"],
            created = source["created"],
        )
    

    def verify_password(self, password: str):
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
