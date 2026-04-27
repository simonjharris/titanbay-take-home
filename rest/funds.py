from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import FundRead, FundCreate, FundUpdate, ErrorDetail
from data.database import DatabaseSession
from exceptions import NotFoundError
import business_logic.funds as fund_logic

fund_router = APIRouter(tags=["funds"])

_404 = {404: {"model": ErrorDetail, "description": "Fund not found"}}


@fund_router.get(
    "/funds",
    summary="List all funds",
    description="Returns a list of all investment funds.",
)
async def get_funds(db: DatabaseSession) -> list[FundRead]:
    return fund_logic.get_all(db)


@fund_router.get(
    "/funds/{fund_id}",
    summary="Get a fund by ID",
    description="Returns a single fund by its UUID. Returns 404 if not found.",
    responses=_404,
)
async def get_fund_by_id(fund_id: UUID, db: DatabaseSession) -> FundRead:
    try:
        return fund_logic.get_by_id(db, fund_id)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@fund_router.post(
    "/funds",
    status_code=status.HTTP_201_CREATED,
    summary="Create a fund",
    description="Creates a new investment fund and returns it.",
)
async def create_fund(fund: FundCreate, db: DatabaseSession) -> FundRead:
    return fund_logic.create(db, fund)


@fund_router.put(
    "/funds",
    summary="Update a fund",
    description=(
        "Updates an existing fund identified by the `id` field in the request body. "
        "Returns 404 if the fund does not exist."
    ),
    responses=_404,
)
async def update_fund(fund: FundUpdate, db: DatabaseSession) -> FundRead:
    # 404 is used here even though the fund id comes from the request body rather than
    # the path. 422 would be the strict alternative, but 404 better expresses the
    # semantics: the referenced resource does not exist. An alternative design would be
    # PUT /funds/{fund_id} to make the 404 unambiguous, but that deviates from the spec.
    try:
        return fund_logic.update(db, fund)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
