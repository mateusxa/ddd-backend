from datetime import datetime, timezone
import hashlib
import os
from domain.entites import Entity
from utils.error import Error



class Admin(Entity):
    
    def __init__(self, name: str, email: str, password: str, id: str | None = None, created: datetime | None = None):
        self._name = name
        self._email = email
        self._password = password
        self._id = id
        self._created = created or datetime.now(timezone.utc)

    @property
    def name(self) -> str:
        return  self._name
    
    @property
    def email(self) -> str:
        return  self._email
    
    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, password):
        self._password = password
    
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
            password={self.password}, \
            id={self._id}, \
            created={self._created}\
        )"

    def is_password_valid(self, password: str):
        if self.hash_password(password) ==  self.password:
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
            password = source["password"],
            created = source["created"],
        )
