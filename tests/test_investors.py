import uuid

from fastapi import status
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from data.data_schemas import InvestorCreate
from data.db_models import Investor
from data.types import InvestorType


def test_get_investors_returns_empty_list(test_client: TestClient) -> None:
    res = test_client.get("/investors")
    assert res.status_code == status.HTTP_200_OK
    assert res.json() == []


def test_get_investors_returns_all(
    test_client: TestClient, database_session: Session
) -> None:
    database_session.add(
        Investor(
            id=uuid.uuid4(),
            name="Alice",
            investor_type=InvestorType.INDIVIDUAL,
            email="alice@example.com",
        )
    )
    database_session.add(
        Investor(
            id=uuid.uuid4(),
            name="Acme Capital",
            investor_type=InvestorType.INSTITUTION,
            email="acme@example.com",
        )
    )
    database_session.flush()

    res = test_client.get("/investors")
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert len(data) == 2
    emails = {i["email"] for i in data}
    assert emails == {"alice@example.com", "acme@example.com"}


def test_create_investor_persists_to_db(test_client: TestClient) -> None:
    payload = InvestorCreate(
        name="Bob",
        investor_type=InvestorType.FAMILY_OFFICE,
        email="bob@example.com",
    )

    create_response = test_client.post(
        "/investors", json=payload.model_dump(mode="json")
    )
    assert create_response.status_code == status.HTTP_201_CREATED

    data = create_response.json()
    assert data["name"] == "Bob"
    assert data["email"] == "bob@example.com"
    assert data["investor_type"] == InvestorType.FAMILY_OFFICE
    assert "id" in data
    assert "created_at" in data


def test_create_investor_duplicate_email_returns_409(
    test_client: TestClient, database_session: Session
) -> None:
    database_session.add(
        Investor(
            id=uuid.uuid4(),
            name="Carol",
            investor_type=InvestorType.INDIVIDUAL,
            email="carol@example.com",
        )
    )
    database_session.flush()

    payload = InvestorCreate(
        name="Carol Duplicate",
        investor_type=InvestorType.INSTITUTION,
        email="carol@example.com",
    )
    res = test_client.post("/investors", json=payload.model_dump(mode="json"))
    assert res.status_code == status.HTTP_409_CONFLICT