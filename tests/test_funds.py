import uuid
from decimal import Decimal
from typing import Any

from fastapi import status
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from data.data_schemas import FundCreate, FundUpdate
from data.db_models import Fund
from data.types import FundStatus


def _make_fund(**kwargs: Any) -> Fund:
    defaults: dict[str, Any] = dict(
        id=uuid.uuid4(),
        name="Test Fund I",
        vintage_year=2024,
        target_size_usd=Decimal("10000000.00"),
        status=FundStatus.FUNDRAISING,
    )
    defaults.update(kwargs)
    return Fund(**defaults)


def test_get_funds_returns_empty_list(test_client: TestClient) -> None:
    res = test_client.get("/funds")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []


def test_get_funds_returns_all(
    test_client: TestClient, database_session: Session
) -> None:
    database_session.add(_make_fund(name="Fund A"))
    database_session.add(_make_fund(name="Fund B"))
    database_session.flush()

    res = test_client.get("/funds")
    assert res.status_code == status.HTTP_200_OK
    names = {f["name"] for f in res.json()}
    assert names == {"Fund A", "Fund B"}


def test_create_fund_persists_to_db(test_client: TestClient) -> None:
    payload = FundCreate(
        name="Test Fund I",
        vintage_year=2024,
        target_size_usd=Decimal("10000000.00"),
        status=FundStatus.FUNDRAISING,
    )

    create_response = test_client.post("/funds", json=payload.model_dump(mode="json"))
    assert create_response.status_code == status.HTTP_201_CREATED

    fund_id = create_response.json()["id"]

    res = test_client.get(f"/funds/{fund_id}")
    assert res.status_code == status.HTTP_200_OK
    response_data = res.json()
    assert response_data["name"] == "Test Fund I"


def test_get_fund_by_id(test_client: TestClient, database_session: Session) -> None:
    fund = _make_fund(name="Test Fund I")
    database_session.add(fund)
    database_session.flush()

    res = test_client.get(f"/funds/{fund.id}")

    response_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert response_data["name"] == "Test Fund I"


def test_get_fund_by_id_does_not_exist_returns_404(
    test_client: TestClient, database_session: Session
) -> None:
    fund_id = uuid.uuid4()
    res = test_client.get(f"/funds/{fund_id}")
    assert res.status_code == status.HTTP_404_NOT_FOUND


def test_update_fund(test_client: TestClient, database_session: Session) -> None:
    fund_id = uuid.uuid4()
    database_session.add(
        _make_fund(id=fund_id, name="Old Name", status=FundStatus.FUNDRAISING)
    )
    database_session.flush()

    payload = FundUpdate(
        id=fund_id,
        name="New Name",
        vintage_year=2024,
        target_size_usd=Decimal("10000000.00"),
        status=FundStatus.INVESTING,
    )
    res = test_client.put("/funds", json=payload.model_dump(mode="json"))
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert data["name"] == "New Name"
    assert data["status"] == FundStatus.INVESTING

    # ensure database updated as expected
    updated_fund = database_session.get(Fund, fund_id)
    assert updated_fund
    assert updated_fund.name == "New Name"
    assert updated_fund.created_at != updated_fund.updated_at


def test_update_fund_not_found_returns_404(test_client: TestClient) -> None:
    payload = FundUpdate(
        id=uuid.uuid4(),
        name="Ghost Fund",
        vintage_year=2020,
        target_size_usd=Decimal("5000000.00"),
        status=FundStatus.CLOSED,
    )
    res = test_client.put("/funds", json=payload.model_dump(mode="json"))
    assert res.status_code == status.HTTP_404_NOT_FOUND
