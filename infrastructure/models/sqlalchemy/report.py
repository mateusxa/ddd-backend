import uuid
from sqlalchemy import CHAR, TIMESTAMP, UUID, ForeignKey, Integer, String, func
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

UniqueIdentifier = UUID(as_uuid=True)

Base = declarative_base()

class ReportModel(Base):
    
    __tablename__ = "admins"

    id: Mapped[uuid.UUID] = mapped_column(Integer, primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey('companies.id'))
    company = relationship("CompanyModel", back_populates="customers")
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    bucket_url: Mapped[str | None] = mapped_column(String(128))
    created: Mapped[str] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
