import uuid
from decimal import Decimal

from fastapi import status
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from data.data_schemas import FundCreate
from data.db_models import Fund
from data.types import FundStatus


def test_create_fund_persists_to_db(test_client: TestClient)->None:
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


def test_get_fund_by_id(test_client: TestClient, database_session: Session)->None:
    fund_id = uuid.uuid4()
    fund_data = FundCreate(
        name="Test Fund I",
        vintage_year=2024,
        target_size_usd=Decimal("10000000.00"),
        status=FundStatus.FUNDRAISING,
    )
    database_session.add(Fund(id=fund_id, **fund_data.model_dump(mode="json")))

    res = test_client.get(f"/funds/{fund_id}")

    response_data = res.json()
    assert res.status_code == status.HTTP_200_OK
    assert response_data["name"] == "Test Fund I"
