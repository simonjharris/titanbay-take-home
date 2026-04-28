from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from data.types import FundStatus, InvestorType


class ErrorDetail(BaseModel):
    detail: str = Field(description="Human-readable error message")


class FundCreate(BaseModel):
    name: str = Field(description="Name of the fund")
    vintage_year: int = Field(description="Year the fund was established")
    target_size_usd: Decimal = Field(description="Target fundraising size in USD")
    status: FundStatus = Field(description="Current fund status: Fundraising, Investing, or Closed")


class FundUpdate(FundCreate):
    id: UUID = Field(description="Unique identifier of the fund to update")


class FundRead(BaseModel):
    id: UUID = Field(description="Unique identifier for the fund")
    name: str = Field(description="Name of the fund")
    vintage_year: int = Field(description="Year the fund was established")
    target_size_usd: Decimal = Field(description="Target fundraising size in USD")
    status: FundStatus = Field(description="Current fund status: Fundraising, Investing, or Closed")
    created_at: datetime = Field(description="Timestamp when the fund was created")

    model_config = ConfigDict(from_attributes=True)


class InvestorCreate(BaseModel):
    name: str = Field(description="Full name of the investor")
    investor_type: InvestorType = Field(description="Type of investor (e.g. Individual, Institution)")
    email: EmailStr = Field(description="Unique email address of the investor")


class InvestorRead(BaseModel):
    id: UUID = Field(description="Unique identifier for the investor")
    name: str = Field(description="Full name of the investor")
    investor_type: InvestorType = Field(description="Type of investor (e.g. Individual, Institution)")
    email: EmailStr = Field(description="Email address of the investor")
    created_at: datetime = Field(description="Timestamp when the investor was registered")

    model_config = ConfigDict(from_attributes=True)


class InvestmentCreate(BaseModel):
    investor_id: UUID = Field(description="ID of the investor making the investment")
    amount_usd: Decimal = Field(description="Investment amount in USD")
    investment_date: date = Field(description="Date the investment was made")


class InvestmentRead(BaseModel):
    id: UUID = Field(description="Unique identifier for the investment")
    investor_id: UUID = Field(description="ID of the investor who made the investment")
    fund_id: UUID = Field(description="ID of the fund the investment belongs to")
    amount_usd: Decimal = Field(description="Investment amount in USD")
    investment_date: date = Field(description="Date the investment was made")

    model_config = ConfigDict(from_attributes=True)