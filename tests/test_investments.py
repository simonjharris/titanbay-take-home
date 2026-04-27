import uuid
from datetime import date
from decimal import Decimal
from typing import Any

import pytest
from fastapi import status
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from data.data_schemas import InvestmentCreate
from data.db_models import Fund, Investor, Investment
from data.types import FundStatus, InvestorType


def _make_fund(database_session: Session, **kwargs: Any) -> Fund:
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        name="Test Fund",
        vintage_year=2024,
        target_size_usd=Decimal("10000000.00"),
        status=FundStatus.FUNDRAISING,
    )
    defaults.update(kwargs)
    fund = Fund(**defaults)
    database_session.add(fund)
    return fund


def _make_investor(database_session: Session, **kwargs: Any) -> Investor:
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        name="Alice",
        investor_type=InvestorType.INDIVIDUAL,
        email=f"investor-{uuid.uuid4()}@example.com",
    )
    defaults.update(kwargs)
    investor = Investor(**defaults)
    database_session.add(investor)
    return investor


def _make_investment(database_session: Session, fund: Fund, investor: Investor, **kwargs: Any) -> Investment:
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        fund_id=fund.id,
        investor_id=investor.id,
        amount_usd=Decimal("500000.00"),
        investment_date=date(2024, 6, 1),
    )
    defaults.update(kwargs)
    investment = Investment(**defaults)
    database_session.add(investment)
    return investment


def test_get_investments_for_fund_returns_empty_list(
    test_client: TestClient, database_session: Session
) -> None:
    fund = _make_fund(database_session)
    database_session.flush()

    res = test_client.get(f"/funds/{fund.id}/investments")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []


def test_get_investments_for_fund_returns_only_that_funds_investments(
    test_client: TestClient, database_session: Session
) -> None:
    fund_a = _make_fund(database_session, name="Fund A")
    fund_b = _make_fund(database_session, name="Fund B")
    investor = _make_investor(database_session)
    investment_a = _make_investment(database_session, fund_a, investor, amount_usd=Decimal("100000.00"))
    _make_investment(database_session, fund_b, investor, amount_usd=Decimal("200000.00"))
    database_session.flush()

    res = test_client.get(f"/funds/{fund_a.id}/investments")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert len(data) == 1
    assert data[0]["id"] == str(investment_a.id)
    assert data[0]["fund_id"] == str(fund_a.id)


def test_get_investments_for_fund_not_found_returns_404(
    test_client: TestClient,
) -> None:
    res = test_client.get(f"/funds/{uuid.uuid4()}/investments")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_get_investments_for_fund_returns_all_for_that_fund(
    test_client: TestClient, database_session: Session
) -> None:
    fund = _make_fund(database_session)
    investor = _make_investor(database_session)
    database_session.flush()
    _make_investment(database_session, fund, investor, amount_usd=Decimal("100000.00"))
    _make_investment(database_session, fund, investor, amount_usd=Decimal("200000.00"))
    database_session.flush()

    res = test_client.get(f"/funds/{fund.id}/investments")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert len(data) == 2
    amounts = {d["amount_usd"] for d in data}
    assert amounts == {"100000.00", "200000.00"}


def test_create_investment_persists_to_db(
    test_client: TestClient, database_session: Session
) -> None:
    fund = _make_fund(database_session)
    investor = _make_investor(database_session)
    database_session.flush()

    payload = InvestmentCreate(
        investor_id=investor.id,
        amount_usd=Decimal("750000.00"),
        investment_date=date(2024, 3, 15),
    )
    res = test_client.post(
        f"/funds/{fund.id}/investments", json=payload.model_dump(mode="json")
    )
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["fund_id"] == str(fund.id)
    assert data["investor_id"] == str(investor.id)
    assert data["amount_usd"] == "750000.00"
    assert data["investment_date"] == "2024-03-15"
    assert "id" in data


def test_create_investment_fund_not_found_returns_404(
    test_client: TestClient, database_session: Session
) -> None:
    investor = _make_investor(database_session)
    database_session.flush()

    unknown_fund_id = uuid.uuid4()
    payload = InvestmentCreate(
        investor_id=investor.id,
        amount_usd=Decimal("100000.00"),
        investment_date=date(2024, 1, 1),
    )
    res = test_client.post(
        f"/funds/{unknown_fund_id}/investments", json=payload.model_dump(mode="json")
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_create_investment_investor_not_found_returns_404(
    test_client: TestClient, database_session: Session
) -> None:
    fund = _make_fund(database_session)
    database_session.flush()

    payload = InvestmentCreate(
        investor_id=uuid.uuid4(),
        amount_usd=Decimal("100000.00"),
        investment_date=date(2024, 1, 1),
    )
    res = test_client.post(
        f"/funds/{fund.id}/investments", json=payload.model_dump(mode="json")
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize("fund_status", [FundStatus.INVESTING, FundStatus.CLOSED])
def test_create_investment_non_fundraising_fund_returns_409(
    test_client: TestClient, database_session: Session, fund_status: FundStatus
) -> None:
    fund = _make_fund(database_session, status=fund_status)
    investor = _make_investor(database_session)
    database_session.flush()

    payload = InvestmentCreate(
        investor_id=investor.id,
        amount_usd=Decimal("100000.00"),
        investment_date=date(2024, 1, 1),
    )
    res = test_client.post(
        f"/funds/{fund.id}/investments", json=payload.model_dump(mode="json")
    )
    assert res.status_code == status.HTTP_409_CONFLICT