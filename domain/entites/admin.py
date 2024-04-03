from datetime import datetime, timezone
from domain.entites import UserEntity
from utils.error import DictIncomplete



class Admin(UserEntity):
    
    name: str
    email: str
    hashed_password: str | None
    id: str | None
    created: datetime


    def __init__(
            self, name: str, email: str, password: str | None = None, hashed_password: str | None = None, 
            id: str | None = None, created: datetime | None = None
        ):
        self.name = name
        self.email = email
        self.hashed_password = self.hash_password(password) if password else hashed_password
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
            self.hashed_password = Admin.hash_password(password)
        return self


    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Admin.__annotations__):
            raise DictIncomplete(source)
        return Admin(
            id = source["id"],
            name = source["name"],
            email = source["email"],
            hashed_password = source["hashed_password"],
            created = source["created"],
        )
