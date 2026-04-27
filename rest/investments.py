from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import InvestmentRead, InvestmentCreate
from data.database import DatabaseSession
from exceptions import NotFoundError
import business_logic.investments as investment_logic

investments_router = APIRouter()


@investments_router.get("/funds/{fund_id}/investments")
async def get_investments_for_fund(
    fund_id: UUID, db: DatabaseSession
) -> list[InvestmentRead]:
    try:
        return investment_logic.get_for_fund(db, fund_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@investments_router.post(
    "/funds/{fund_id}/investments", status_code=status.HTTP_201_CREATED
)
async def create_investment_for_fund(
    fund_id: UUID, investment_data: InvestmentCreate, db: DatabaseSession
) -> InvestmentRead:
    # 404 covers both fund (path param) and investor (body param) not found.
    # See comment on PUT /funds for rationale on using 404 for body-referenced resources.
    try:
        return investment_logic.create(db, fund_id, investment_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
