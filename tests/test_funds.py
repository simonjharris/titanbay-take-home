from fastapi import status


def test_create_fund_persists_to_db(client):
    payload = {
        "name": "Test Fund I",
        "vintage_year": 2024,
        "target_size_usd": "10000000.00",
        "status": "Fundraising",
    }

    create_response = client.post("/funds", json=payload)
    assert create_response.status_code == status.HTTP_201_CREATED

    fund_id = create_response.json()["id"]

    get_response = client.get(f"/funds/{fund_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["name"] == "Test Fund I"
