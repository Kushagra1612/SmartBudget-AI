"""
Integration tests for /budgets -- full CRUD plus the summary endpoint.
"""

import uuid
from datetime import date
from decimal import Decimal

from app.models.statement import Statement
from app.models.transaction import Transaction, TransactionCategory, TransactionType


def _budget_payload(**overrides):
    today = date.today()
    payload = {
        "category": "Food",
        "monthly_limit": "5000",
        "month": today.month,
        "year": today.year,
    }
    payload.update(overrides)
    return payload


def test_requires_authentication(client):
    response = client.post("/budgets", json=_budget_payload())
    assert response.status_code == 401


def test_create_budget(client, auth_headers):
    response = client.post("/budgets", json=_budget_payload(), headers=auth_headers)

    assert response.status_code == 201
    body = response.json()
    assert body["category"] == "Food"
    assert float(body["monthly_limit"]) == 5000


def test_create_budget_rejects_a_non_positive_limit(client, auth_headers):
    response = client.post(
        "/budgets",
        json=_budget_payload(monthly_limit="0"),
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_list_budgets_for_a_month(client, auth_headers):
    client.post("/budgets", json=_budget_payload(), headers=auth_headers)
    today = date.today()

    response = client.get(
        f"/budgets/?month={today.month}&year={today.year}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["category"] == "Food"


def test_budget_summary_reflects_zero_spend_with_no_transactions(
    client, auth_headers
):
    client.post("/budgets", json=_budget_payload(), headers=auth_headers)
    today = date.today()

    response = client.get(
        f"/budgets/summary?month={today.month}&year={today.year}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    summary = response.json()[0]
    assert float(summary["spent"]) == 0
    assert float(summary["remaining"]) == 5000


def test_get_a_single_budget(client, auth_headers):
    created = client.post(
        "/budgets", json=_budget_payload(), headers=auth_headers
    ).json()

    response = client.get(f"/budgets/{created['id']}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_a_user_cannot_access_another_users_budget(
    client, auth_headers, user_credentials
):
    created = client.post(
        "/budgets", json=_budget_payload(), headers=auth_headers
    ).json()

    other_credentials = dict(user_credentials, email="other_budget_user@example.com")
    client.post("/auth/register", json=other_credentials)
    other_login = client.post(
        "/auth/login",
        data={
            "username": other_credentials["email"],
            "password": other_credentials["password"],
        },
    )
    other_headers = {
        "Authorization": f"Bearer {other_login.json()['access_token']}"
    }

    response = client.get(f"/budgets/{created['id']}", headers=other_headers)
    assert response.status_code == 403


def test_update_budget(client, auth_headers):
    created = client.post(
        "/budgets", json=_budget_payload(), headers=auth_headers
    ).json()

    response = client.put(
        f"/budgets/{created['id']}",
        json={"category": "Food", "monthly_limit": "7500"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert float(response.json()["monthly_limit"]) == 7500


def test_delete_budget(client, auth_headers):
    created = client.post(
        "/budgets", json=_budget_payload(), headers=auth_headers
    ).json()

    delete_response = client.delete(f"/budgets/{created['id']}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/budgets/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 404


def test_a_budget_lands_in_the_statement_month_not_todays_real_date(
    client, auth_headers, registered_user, db_session
):
    """
    Regression test for the actual bug this change fixes: budgets used
    to always be created against today's real calendar date, even when
    the user's only uploaded statement was for a different month -- so
    a freshly created budget could never show any spending against it,
    since the spending lived in the statement's month and the budget
    lived in today's.

    Any client-sent month/year is now ignored entirely (BudgetCreate no
    longer even has those fields) -- BudgetService.create_budget always
    resolves through StatementService.resolve_period(), the same helper
    Dashboard already used, so a statement's month always wins.
    """

    past_month, past_year = 3, 2024
    user_id = uuid.UUID(registered_user["id"])

    statement = Statement(
        user_id=user_id,
        filename="old_statement.pdf",
        original_filename="old_statement.pdf",
        month=past_month,
        year=past_year,
    )
    db_session.add(statement)
    db_session.commit()
    db_session.refresh(statement)

    db_session.add(
        Transaction(
            user_id=user_id,
            statement_id=statement.id,
            amount=Decimal("400"),
            transaction_type=TransactionType.EXPENSE,
            category=TransactionCategory.FOOD,
            merchant="Old Merchant",
            source="manual",
            transaction_date=date(past_year, past_month, 15),
        )
    )
    db_session.commit()

    created = client.post(
        "/budgets",
        json={"category": "Food", "monthly_limit": "1000"},
        headers=auth_headers,
    ).json()

    # The budget was created for the statement's month, not today's.
    assert created["month"] == past_month
    assert created["year"] == past_year

    # And /budgets/summary -- called with no query params at all, the
    # way the frontend now calls it -- finds the spending, because it
    # resolves to that same month instead of today's empty one.
    summary = client.get("/budgets/summary", headers=auth_headers).json()

    assert len(summary) == 1
    assert float(summary[0]["spent"]) == 400
    assert float(summary[0]["remaining"]) == 600
