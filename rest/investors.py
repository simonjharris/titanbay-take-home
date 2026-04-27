from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import InvestorRead, InvestorCreate, ErrorDetail
from data.database import DatabaseSession
from exceptions import ConflictError
import business_logic.investors as investor_logic

investors_router = APIRouter(tags=["investors"])

_409 = {409: {"model": ErrorDetail, "description": "An investor with this email already exists"}}


@investors_router.get(
    "/investors",
    summary="List all investors",
    description="Returns a list of all registered investors.",
)
async def get_investors(db: DatabaseSession) -> list[InvestorRead]:
    return investor_logic.get_all(db)


@investors_router.post(
    "/investors",
    status_code=status.HTTP_201_CREATED,
    summary="Create an investor",
    description=(
        "Registers a new investor. Returns 409 if an investor with the same email "
        "already exists."
    ),
    responses=_409,
)
async def create_investor(
    investor: InvestorCreate, db: DatabaseSession
) -> InvestorRead:
    try:
        return investor_logic.create(db, investor)
    except ConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))