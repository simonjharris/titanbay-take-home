from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from data.data_schemas import FundCreate, FundUpdate
from data.db_models import Fund
from exceptions import NotFoundError


def get_all(db: Session) -> list[Fund]:
    return list(db.execute(select(Fund)).scalars().all())


def get_by_id(db: Session, fund_id: UUID) -> Fund:
    fund = db.get(Fund, fund_id)
    if fund is None:
        raise NotFoundError("Fund")
    return fund


def create(db: Session, data: FundCreate) -> Fund:
    fund = Fund(**data.model_dump())
    db.add(fund)
    db.flush()
    return fund


def update(db: Session, data: FundUpdate) -> Fund:
    fund = db.get(Fund, data.id)
    if fund is None:
        raise NotFoundError("Fund")
    for field, value in data.model_dump(exclude={"id"}).items():
        setattr(fund, field, value)
    db.flush()
    return fund