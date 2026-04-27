# Fund
# Field	Type	Description
# id	string (uuid)	Unique identifier for the fund
# name	string	Name of the fund
# vintage_year	integer	Year the fund was established
# target_size_usd	number (decimal)	Target size of the fund in USD
# status	string	Fund status: Fundraising, Investing, or Closed
# created_at	string (date-time)	Timestamp when the fund was created
#
from datetime import datetime, date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

from data.types import FundStatus, InvestorType


class FundCreate(BaseModel):
    name: str
    vintage_year: int
    target_size_usd: Decimal
    status: FundStatus


class FundUpdate(FundCreate):
    id: UUID


class FundRead(BaseModel):
    id: UUID
    name: str
    vintage_year: int
    target_size_usd: Decimal
    status: FundStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvestorCreate(BaseModel):
    name: str
    investor_type: InvestorType
    email: EmailStr


class InvestorRead(BaseModel):
    id: UUID
    name: str
    investor_type: InvestorType
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvestmentCreate(BaseModel):
    investor_id: UUID
    amount_usd: Decimal
    investment_date: date


class InvestmentRead(BaseModel):
    id: UUID
    investor_id: UUID
    fund_id: UUID
    amount_usd: Decimal
    investment_date: date

    model_config = ConfigDict(from_attributes=True)
