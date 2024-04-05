from datetime import datetime, timezone
import hashlib
import os
from domain.entites import Entity
from utils.error import Error



class Admin(Entity):
    
    def __init__(
            self, name: str, email: str, password: str | None = None, hashed_password: str | None = None, 
            id: str | None = None, created: datetime | None = None
        ):
        self._name = name
        self._email = email
        self._hashed_password = self.hash_password(password) if password else hashed_password
        self._id = id
        self._created = created or datetime.now(timezone.utc)

    @property
    def name(self) -> str:
        return  self._name
    
    @property
    def email(self) -> str:
        return  self._email
    
    @property
    def hashed_password(self) -> str | None:
        return self._hashed_password
    
    @hashed_password.setter
    def hashed_password(self, password: str):
        self._hashed_password = Admin.hash_password(password)
    
    @property
    def id(self) -> str | None:
        return  self._id
    
    @property
    def created(self) -> datetime:
        return  self._created

    def __repr__(self):
        return f"Admin(\
            name={self._name}, \
            email={self._email}, \
            hashed_password={self.hashed_password}, \
            id={self._id}, \
            created={self._created}\
        )"

    def is_password_valid(self, password: str):
        if self.hash_password(password) ==  self.hashed_password:
            self.verified = True
            return True
        return False

    @staticmethod
    def hash_password(password: str) -> str:
        salted_password = f"{password}:{os.environ['PASSWORD_JWT_SECRET']}".encode('utf-8')
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(salted_password)        
        return hash_algorithm.hexdigest()

    @staticmethod
    def from_dict(source: dict):
        if not all(attr in source for attr in Admin.__annotations__):
            raise Error(Error.Code.internal_error, str(source), 500)
        return Admin(
            id = source["id"],
            name = source["name"],
            email = source["email"],
            hashed_password = source["hashed_password"],
            created = source["created"],
        )
