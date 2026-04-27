from fastapi import APIRouter
from starlette import status

from data.data_schemas import InvestorRead, InvestorCreate

investors_router = APIRouter()

@investors_router.get("/investors")
async def get_investors() -> list[InvestorRead]:
    pass


@investors_router.post("/investors", status_code=status.HTTP_201_CREATED)
async def create_investor(investor: InvestorCreate) -> InvestorRead:
    pass