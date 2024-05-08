import uuid
from sqlalchemy import CHAR, TIMESTAMP, UUID, Integer, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

UniqueIdentifier = UUID(as_uuid=True)

Base = declarative_base()

class AdminModel(Base):
    
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) # mapped_column(CHAR(36), primary_key=True, default=str(uuid.uuid4()), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
