import uuid
from datetime import datetime, date, timezone
from decimal import Decimal
from sqlalchemy import func, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from data.types import FundStatus, InvestorType


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4()
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=lambda: datetime.now(timezone.utc)
    )


class Fund(Base):
    __tablename__ = "funds"
    name: Mapped[str]
    vintage_year: Mapped[int]
    target_size_usd: Mapped[Decimal]
    status: Mapped[FundStatus]
    investments: Mapped[list["Investment"]] = relationship(back_populates="fund")


class Investor(Base):
    __tablename__ = "investors"
    name: Mapped[str]
    investor_type: Mapped[InvestorType]
    email: Mapped[str] = mapped_column(unique=True)
    investments: Mapped[list["Investment"]] = relationship(back_populates="investor")


class Investment(Base):
    __tablename__ = "investments"
    fund_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("funds.id")
    )
    investor_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("investors.id")
    )
    amount_usd: Mapped[Decimal]
    investment_date: Mapped[date]
    fund: Mapped["Fund"] = relationship(back_populates="investments")
    investor: Mapped["Investor"] = relationship(back_populates="investments")
