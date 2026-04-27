from fastapi import APIRouter
from starlette import status

from data.data_schemas import InvestmentRead, InvestmentCreate

investments_router = APIRouter()

@investments_router.get("/funds/{fund_id}/investments")
async def get_investments_for_fund(fund_id: str)->list[InvestmentRead]:
    pass



@investments_router.post("/funds/{fund_id}/investments", status_code=status.HTTP_201_CREATED)
async def create_investment_for_fund(investment_data: InvestmentCreate)->InvestmentRead:
    pass

