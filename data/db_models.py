import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, Column, UUID, Enum
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from data.types import FundStatus


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(),server_onupdate=func.now())

class Fund(Base):
    __tablename__ = "funds"
    name: Mapped[str]
    vintage_year: Mapped[int]
    target_size_usd: Mapped[Decimal]
    status: Mapped[FundStatus]
