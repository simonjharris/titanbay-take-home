from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.data_schemas import InvestmentCreate, InvestmentRead
from data.db_models import Fund, Investor, Investment
from exceptions import NotFoundError


def get_for_fund(db: Session, fund_id: UUID) -> list[InvestmentRead]:
    if db.get(Fund, fund_id) is None:
        raise NotFoundError("Fund")
    investments = (
        db.execute(select(Investment).where(Investment.fund_id == fund_id))
        .scalars()
        .all()
    )
    return TypeAdapter(list[InvestmentRead]).validate_python(
        investments, from_attributes=True
    )


def create(db: Session, fund_id: UUID, data: InvestmentCreate) -> InvestmentRead:
    if db.get(Fund, fund_id) is None:
        raise NotFoundError("Fund")
    if db.get(Investor, data.investor_id) is None:
        raise NotFoundError("Investor")
    investment_data = data.model_dump()
    investment_data["fund_id"] = fund_id
    investment = Investment(**investment_data)
    db.add(investment)
    db.flush()
    return InvestmentRead.model_validate(investment)
