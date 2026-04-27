from pydantic import TypeAdapter
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from data.data_schemas import InvestorCreate, InvestorRead
from data.db_models import Investor
from exceptions import ConflictError


def get_all(db: Session) -> list[InvestorRead]:
    investors = db.execute(select(Investor)).scalars().all()
    return TypeAdapter(list[InvestorRead]).validate_python(
        investors, from_attributes=True
    )


def create(db: Session, data: InvestorCreate) -> InvestorRead:
    investor = Investor(**data.model_dump())
    db.add(investor)
    try:
        db.flush()
    except IntegrityError:
        raise ConflictError(f"An investor with email '{data.email}' already exists")
    return InvestorRead.model_validate(investor)
