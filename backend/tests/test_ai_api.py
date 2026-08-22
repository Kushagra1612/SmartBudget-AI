"""
Integration tests for /ai/pulse, /ai/advice, /ai/chat.

Gemini is mocked via the mock_gemini fixture -- these test the plumbing
(auth, analytics assembly, request/response shape) rather than what
Gemini actually says, which isn't something a test should assert on
anyway.
"""

from datetime import date

from app.models.transaction import TransactionCategory, TransactionType
from tests.conftest import seed_transactions


def _seed_some_spending(db_session, user_id):
    seed_transactions(
        db_session,
        user_id=user_id,
        count=5,
        category=TransactionCategory.FOOD,
        amount_range=(300, 600),
        transaction_type=TransactionType.EXPENSE,
    )
    seed_transactions(
        db_session,
        user_id=user_id,
        count=1,
        category=TransactionCategory.SALARY,
        amount_range=(40000, 40000),
        transaction_type=TransactionType.INCOME,
    )


def test_pulse_requires_authentication(client):
    response = client.get("/ai/pulse")
    assert response.status_code == 401


def test_pulse_returns_a_message_and_status(
    client, auth_headers, registered_user, db_session, mock_gemini, clean_ai_memory
):
    _seed_some_spending(db_session, registered_user["id"])
    today = date.today()

    response = client.get(
        f"/ai/pulse?month={today.month}&year={today.year}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert "message" in body
    assert "status" in body


def test_advice_returns_the_mocked_response(
    client, auth_headers, registered_user, db_session, mock_gemini, clean_ai_memory
):
    _seed_some_spending(db_session, registered_user["id"])
    today = date.today()

    response = client.post(
        "/ai/advice",
        json={"month": today.month, "year": today.year},
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["advice"] == mock_gemini
    # advice always wants the full picture -- no routing decision to make
    assert set(body["agents_used"]) == {"dashboard", "budget", "spending"}


def test_chat_returns_a_response(
    client, auth_headers, registered_user, db_session, mock_gemini, clean_ai_memory
):
    _seed_some_spending(db_session, registered_user["id"])
    today = date.today()

    response = client.post(
        "/ai/chat",
        json={
            "message": "Where am I overspending?",
            "month": today.month,
            "year": today.year,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["response"] == mock_gemini
    # the mocked Gemini reply isn't valid JSON, so the coordinator's
    # parse fails and falls back to ["dashboard"] -- same fallback the
    # old Planner used
    assert body["agents_used"] == ["dashboard"]


def test_chat_requires_authentication(client):
    response = client.post(
        "/ai/chat",
        json={"message": "Hi", "month": 1, "year": 2026},
    )
    assert response.status_code == 401
