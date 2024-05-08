from abc import ABC, abstractmethod
from base64 import b64decode, b64encode
from infrastructure.models.sqlalchemy.admin import Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from domain.entites import Entity


class Repository(ABC):


    def __init__(self):
        engine = create_engine("mysql+pymysql://root:admin@localhost/db", echo=True)
        if not database_exists(engine.url): 
            create_database(engine.url)
        Base.metadata.create_all(engine)
        self.session = Session(engine)


    @abstractmethod
    def create(self, entity: Entity) -> Entity:
        pass


    @abstractmethod
    def get_by_id(self, entity_id: str) -> Entity | None:
        pass


    @abstractmethod
    def page(self, cursor: str | None = None, limit: int | None = None, **kwargs)-> tuple[str | None, list[Entity]]:
        pass


    @abstractmethod
    def update(self, entity: Entity) -> Entity:
        pass


    @abstractmethod
    def delete(self, entity: Entity) -> None:
        pass

    @staticmethod
    def decode_cursor(cursor: str | None) -> str:
        return b64decode(cursor).decode("utf-8") if cursor else "0"
    
    @staticmethod
    def encode_cursor(cursor: str | None) -> str | None:
        return b64encode(cursor.encode("utf-8")).decode("utf-8") if cursor else None