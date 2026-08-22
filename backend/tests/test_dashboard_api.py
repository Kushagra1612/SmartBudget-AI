"""
Integration tests for GET /dashboard.
"""

from datetime import date

from app.models.transaction import TransactionCategory, TransactionType
from tests.conftest import seed_transactions


def test_requires_authentication(client):
    response = client.get("/dashboard")
    assert response.status_code == 401


def test_returns_zeroed_data_for_a_month_with_no_transactions(client, auth_headers):
    today = date.today()

    response = client.get(
        f"/dashboard?month={today.month}&year={today.year}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert float(body["analytics"]["savings"]["income"]) == 0
    assert float(body["analytics"]["spending"]["total_expense"]) == 0


def test_reflects_seeded_income_and_expenses(
    client, auth_headers, registered_user, db_session
):
    today = date.today()

    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=3,
        category=TransactionCategory.FOOD,
        amount_range=(500, 500),
        transaction_type=TransactionType.EXPENSE,
        start_days_ago=1,
    )
    seed_transactions(
        db_session,
        user_id=registered_user["id"],
        count=1,
        category=TransactionCategory.SALARY,
        amount_range=(40000, 40000),
        transaction_type=TransactionType.INCOME,
        start_days_ago=1,
    )

    response = client.get(
        f"/dashboard?month={today.month}&year={today.year}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert float(body["analytics"]["spending"]["total_expense"]) == 1500
    assert float(body["analytics"]["savings"]["income"]) == 40000


def test_no_statement_and_no_month_year_falls_back_to_todays_data(
    client, auth_headers
):
    """
    Used to be a documented 500: with no uploaded statement and no
    explicit month/year, DashboardService raised a plain ValueError that
    nothing in routers/dashboard.py caught.

    Fixed by StatementService.resolve_period(), the shared helper that
    now also backs Budgets and the AI endpoints: with no statement and
    nothing explicit given, it falls back to today's real calendar date
    instead of raising, so a brand-new user just sees a zeroed dashboard
    for the current month rather than an error page.
    """

    response = client.get("/dashboard", headers=auth_headers)

    assert response.status_code == 200
    body = response.json()
    assert float(body["analytics"]["savings"]["income"]) == 0
    assert float(body["analytics"]["spending"]["total_expense"]) == 0
