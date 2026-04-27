from uuid import UUID

from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import FundRead, FundCreate, FundUpdate
from data.database import DatabaseSession
from exceptions import NotFoundError
import business_logic.funds as fund_logic

fund_router = APIRouter(tags=["funds"])


@fund_router.get("/funds")
async def get_funds(db: DatabaseSession) -> list[FundRead]:
    return fund_logic.get_all(db)


@fund_router.get("/funds/{fund_id}")
async def get_fund_by_id(fund_id: UUID, db: DatabaseSession) -> FundRead:
    try:
        return fund_logic.get_by_id(db, fund_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@fund_router.post("/funds", status_code=status.HTTP_201_CREATED)
async def create_fund(fund: FundCreate, db: DatabaseSession) -> FundRead:
    return fund_logic.create(db, fund)


@fund_router.put("/funds")
async def update_fund(fund: FundUpdate, db: DatabaseSession) -> FundRead:
    # 404 is used here even though the fund id comes from the request body rather than
    # the path. 422 would be the strict alternative, but 404 better expresses the
    # semantics: the referenced resource does not exist. An alternative design would be
    # PUT /funds/{fund_id} to make the 404 unambiguous, but that deviates from the spec.
    try:
        return fund_logic.update(db, fund)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
