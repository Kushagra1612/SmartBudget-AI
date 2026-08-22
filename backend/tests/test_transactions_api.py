"""
Integration tests for GET /transactions.
"""

from tests.conftest import seed_transactions


def test_requires_authentication(client):
    response = client.get("/transactions")
    assert response.status_code == 401


def test_returns_an_empty_list_with_no_transactions(client, auth_headers):
    response = client.get("/transactions", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []


def test_returns_the_users_transactions_newest_first(
    client, auth_headers, registered_user, db_session
):
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=5,
        start_days_ago=1,
    )

    response = client.get("/transactions", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 5

    dates = [t["transaction_date"] for t in body]
    assert dates == sorted(dates, reverse=True)


def test_only_returns_the_current_users_own_transactions(
    client, auth_headers, registered_user, db_session, user_credentials
):
    other_credentials = dict(user_credentials, email="other_txn_user@example.com")
    register_response = client.post("/auth/register", json=other_credentials)
    other_user_id = register_response.json()["id"]

    seed_transactions(db_session, user_id=other_user_id, count=3)

    response = client.get("/transactions", headers=auth_headers)

    assert response.status_code == 200
    assert response.json() == []
