import uuid
from sqlalchemy import CHAR, TIMESTAMP, UUID, ForeignKey, Integer, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

UniqueIdentifier = UUID(as_uuid=True)

Base = declarative_base()

class CustomerModel(Base):
    
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('companies.id'))
    company = relationship("CompanyModel", back_populates="customers")
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
