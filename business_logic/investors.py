from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.data_schemas import InvestorCreate
from data.db_models import Investor
from exceptions import ConflictError


def get_all(db: Session) -> list[Investor]:
    return list(db.execute(select(Investor)).scalars().all())


def create(db: Session, data: InvestorCreate) -> Investor:
    investor = Investor(**data.model_dump())
    db.add(investor)
    try:
        db.flush()
    except IntegrityError:
        raise ConflictError(f"An investor with email '{data.email}' already exists")
    return investor