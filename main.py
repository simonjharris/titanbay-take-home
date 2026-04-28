from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from rest.funds import fund_router
from rest.investments import investments_router
from rest.investors import investors_router

app = FastAPI(
    title="TitanBay Fund Management API",
    description="API for managing investment funds, investors, and investments.",
    version="1.0.0",
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


app.include_router(fund_router)
app.include_router(investments_router)
app.include_router(investors_router)
