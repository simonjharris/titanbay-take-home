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
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, EmailStr





class FundRead(BaseModel):
    id: UUID
    name: str
    vintage_year: int
    target_size_usd: Decimal
    status: FundStatus
    created_at: datetime


class InvestorRead(BaseModel):
    id: UUID
    name: str
    investor_type: InvestorType
    email: EmailStr
    created_at: datetime


class InvestmentRead(BaseModel):
    id: UUID
    investor_id: UUID
    fund_id: UUID
    amount_usd: Decimal
    investment_date: date
