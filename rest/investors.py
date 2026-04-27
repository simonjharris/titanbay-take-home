from fastapi import APIRouter, HTTPException
from starlette import status

from data.data_schemas import InvestorRead, InvestorCreate
from data.database import DatabaseSession
from exceptions import ConflictError
import business_logic.investors as investor_logic

investors_router = APIRouter()


@investors_router.get("/investors")
async def get_investors(db: DatabaseSession) -> list[InvestorRead]:
    return investor_logic.get_all(db)


@investors_router.post("/investors", status_code=status.HTTP_201_CREATED)
async def create_investor(investor: InvestorCreate, db: DatabaseSession) -> InvestorRead:
    try:
        return investor_logic.create(db, investor)
    except ConflictError as e:
        raise HTTPException(status_code=409, detail=str(e))