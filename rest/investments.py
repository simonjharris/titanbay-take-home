from typing import Any
from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import InvestmentRead, InvestmentCreate, ErrorDetail
from data.database import DatabaseSession
from exceptions import ConflictError, NotFoundError
import business_logic.investments as investment_logic

investments_router = APIRouter(tags=["investments"])

_404: dict[int | str, dict[str, Any]] = {404: {"model": ErrorDetail, "description": "Fund or investor not found"}}
_409: dict[int | str, dict[str, Any]] = {
    409: {
        "model": ErrorDetail,
        "description": (
            "Conflict: either the fund is not currently accepting investments "
            "(status is not Fundraising), or this investor has already invested in the fund"
        ),
    }
}


@investments_router.get(
    "/funds/{fund_id}/investments",
    summary="List investments for a fund",
    description="Returns all investments belonging to the specified fund. Returns 404 if the fund does not exist.",
    responses=_404,
)
async def get_investments_for_fund(
    fund_id: UUID, db: DatabaseSession
) -> list[InvestmentRead]:
    try:
        return investment_logic.get_for_fund(db, fund_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@investments_router.post(
    "/funds/{fund_id}/investments",
    status_code=status.HTTP_201_CREATED,
    summary="Create an investment in a fund",
    description=(
        "Records a new investment by an investor into the specified fund. "
        "Returns 404 if the fund or investor does not exist, "
        "409 if the fund is not accepting investments."
    ),
    responses={**_404, **_409},
)
async def create_investment_for_fund(
    fund_id: UUID, investment_data: InvestmentCreate, db: DatabaseSession
) -> InvestmentRead:
    # 404 covers both fund (path param) and investor (body param) not found.
    # See comment on PUT /funds for rationale on using 404 for body-referenced resources.
    try:
        return investment_logic.create(db, fund_id, investment_data)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
