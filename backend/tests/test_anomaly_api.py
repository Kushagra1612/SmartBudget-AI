"""
Integration tests for GET /anomalies -- the full chain: real HTTP
request, real auth, real Postgres, real IsolationForest run over seeded
transactions.
"""

from app.ml.anomaly_detector import MIN_TRANSACTIONS_FOR_DETECTION
from app.models.transaction import TransactionCategory
from tests.conftest import seed_transactions


def test_requires_authentication(client):
    response = client.get("/anomalies")

    assert response.status_code == 401


def test_reports_insufficient_data_below_the_threshold(
    client, auth_headers, registered_user, db_session
):
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=MIN_TRANSACTIONS_FOR_DETECTION - 5,
    )

    response = client.get("/anomalies", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()
    assert body["insufficient_data"] is True
    assert body["anomalies"] == []
    assert str(MIN_TRANSACTIONS_FOR_DETECTION) in body["message"]


def test_flags_an_unusual_transaction_once_past_the_threshold(
    client, auth_headers, registered_user, db_session
):
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=25,
        category=TransactionCategory.FOOD,
        amount_range=(300, 600),
    )
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=1,
        category=TransactionCategory.FOOD,
        amount_range=(18000, 18000),
        start_days_ago=3,
    )

    response = client.get("/anomalies", headers=auth_headers)

    assert response.status_code == 200

    body = response.json()
    assert body["insufficient_data"] is False
    assert len(body["anomalies"]) >= 1

    flagged_amounts = {float(a["amount"]) for a in body["anomalies"]}
    assert 18000.0 in flagged_amounts


def test_rescanning_does_not_create_duplicate_anomaly_records(
    client, auth_headers, registered_user, db_session
):
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=25,
        category=TransactionCategory.FOOD,
        amount_range=(300, 600),
    )
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=1,
        category=TransactionCategory.FOOD,
        amount_range=(18000, 18000),
        start_days_ago=3,
    )

    first = client.get("/anomalies", headers=auth_headers).json()
    second = client.get("/anomalies", headers=auth_headers).json()

    assert len(first["anomalies"]) == len(second["anomalies"])

    first_ids = {a["id"] for a in first["anomalies"]}
    second_ids = {a["id"] for a in second["anomalies"]}
    assert first_ids == second_ids


def test_only_sees_the_current_users_own_transactions(
    client, auth_headers, registered_user, db_session, user_credentials
):
    # Seed a second user with their own huge outlier, and confirm the
    # first user's scan never sees it.
    other_credentials = dict(user_credentials, email="someone_else@example.com")
    register_response = client.post("/auth/register", json=other_credentials)
    other_user_id = register_response.json()["id"]

    seed_transactions(
        db_session,
        user_id=other_user_id,
        count=25,
        category=TransactionCategory.FOOD,
        amount_range=(300, 600),
    )
    seed_transactions(
        db_session,
        user_id=other_user_id,
        count=1,
        category=TransactionCategory.FOOD,
        amount_range=(50000, 50000),
        start_days_ago=3,
    )

    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=MIN_TRANSACTIONS_FOR_DETECTION - 5,
    )

    response = client.get("/anomalies", headers=auth_headers)
    body = response.json()

    # Still below this user's own threshold -- the other user's data,
    # anomalous or not, must never leak into this count or this result.
    assert body["insufficient_data"] is True
    assert body["anomalies"] == []
