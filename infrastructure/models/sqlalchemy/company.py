import uuid
from sqlalchemy import TIMESTAMP, UUID, Integer, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

UniqueIdentifier = UUID(as_uuid=True)

Base = declarative_base()

class CompanyModel(Base):
    
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    tax_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    customers = relationship("CustomerModel", back_populates="companies")
    reports = relationship("ReportModel", back_populates="companies")
