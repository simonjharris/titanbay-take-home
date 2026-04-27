from uuid import UUID

from fastapi import APIRouter
from starlette import status

from data.data_schemas import FundRead, FundCreate

fund_router = APIRouter(tags=["funds"])

@fund_router.get("/funds")
async def get_funds()->list[FundRead]:
    pass

@fund_router.get("/funds/{fund_id}")
async def get_fund_by_id(fund_id: UUID)->FundRead:
    pass

@fund_router.post("/funds", status_code=status.HTTP_201_CREATED)
async def create_fund(fund: FundCreate)->FundRead:
    pass

@fund_router.put("/funds")
async def update_fund(fund: FundCreate)->FundRead:
    pass