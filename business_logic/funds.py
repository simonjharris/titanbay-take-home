from uuid import UUID

from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.orm import Session

from data.data_schemas import FundCreate, FundRead, FundUpdate
from data.db_models import Fund
from exceptions import NotFoundError


def get_all(db: Session) -> list[FundRead]:
    funds = db.execute(select(Fund)).scalars().all()
    return TypeAdapter(list[FundRead]).validate_python(funds, from_attributes=True)


def get_by_id(db: Session, fund_id: UUID) -> FundRead:
    fund = db.get(Fund, fund_id)
    if fund is None:
        raise NotFoundError("Fund")
    return FundRead.model_validate(fund)


def create(db: Session, data: FundCreate) -> FundRead:
    fund = Fund(**data.model_dump())
    db.add(fund)
    db.flush()
    return FundRead.model_validate(fund)


def update(db: Session, data: FundUpdate) -> FundRead:
    fund = db.get(Fund, data.id)
    if fund is None:
        raise NotFoundError("Fund")
    for field, value in data.model_dump(exclude={"id"}).items():
        setattr(fund, field, value)
    db.flush()
    return FundRead.model_validate(fund)
