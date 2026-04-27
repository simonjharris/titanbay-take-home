from fastapi import FastAPI
from sqlalchemy import JSON

from rest.funds import fund_router
from rest.investments import investments_router
from rest.investors import investors_router

app = FastAPI()

app.include_router(fund_router)
app.include_router(investments_router)
app.include_router(investors_router)

