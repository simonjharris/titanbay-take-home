from fastapi import FastAPI

from rest.funds import fund_router
from rest.investments import investments_router
from rest.investors import investors_router

app=FastAPI()

app.include_router(fund_router)
app.include_router(investments_router)
app.include_router(investors_router)

@app.get("/health")
def health():
    return {"status": "ok"}