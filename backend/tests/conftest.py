
import os
import random
import uuid
from datetime import date, timedelta
from decimal import Decimal

# Has to happen before any `app.*` import: app/config.py reads
# DATABASE_URL at import time, and app/database/database.py creates the
# engine at import time too. Setting this first means every test runs
# against the test database, never your real one.
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/smart_budget_ai_test",
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importing app.main first (rather than reaching into app.models.*
# directly) sidesteps a partial-module import-order issue between
# app.database and app.models -- see PHASE_10_NOTES.md.
from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.models.statement import Statement
from app.models.transaction import Transaction, TransactionCategory, TransactionType

TEST_DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture(scope="session", autouse=True)
def _test_schema():
    """Fresh schema once per test run, torn down at the end."""

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def _clean_tables(_test_schema):
    """
    Every test starts from empty tables. Simpler and more predictable
    than sharing one rolled-back transaction between a test's direct DB
    access and the TestClient's own request-scoped sessions.
    """

    yield

    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    """FastAPI TestClient wired to the test database."""

    app.dependency_overrides[get_db] = _override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def db_session():

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def user_credentials():
    """A unique set of register/login credentials, fresh per test."""

    unique = uuid.uuid4().hex[:8]

    return {
        "full_name": "Test User",
        "email": f"test_{unique}@example.com",
        "password": "testpassword123",
    }


@pytest.fixture()
def registered_user(client, user_credentials):
    response = client.post("/auth/register", json=user_credentials)
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture()
def auth_headers(client, registered_user, user_credentials):
    response = client.post(
        "/auth/login",
        data={
            "username": user_credentials["email"],
            "password": user_credentials["password"],
        },
    )
    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def mock_gemini(monkeypatch):

    from app.ai.gemini_service import GeminiService

    canned_response = "This is a mocked AI response for testing."

    def fake_generate(self, prompt: str) -> str:
        return canned_response

    monkeypatch.setattr(GeminiService, "generate", fake_generate)

    return canned_response


@pytest.fixture()
def clean_ai_memory():

    from app.services.ai_service import AIService

    AIService._memories.clear()
    yield
    AIService._memories.clear()


def seed_transactions(
    db_session,
    *,
    user_id,
    count,
    category: TransactionCategory = TransactionCategory.FOOD,
    amount_range: tuple[int, int] = (300, 600),
    transaction_type: TransactionType = TransactionType.EXPENSE,
    start_days_ago: int = 1,
    same_day: bool = False,
):
   

    if isinstance(user_id, str):
        user_id = uuid.UUID(user_id)

    statement = Statement(
        user_id=user_id,
        filename="test_statement.pdf",
        original_filename="test_statement.pdf",
        month=date.today().month,
        year=date.today().year,
    )
    db_session.add(statement)
    db_session.commit()
    db_session.refresh(statement)

    transactions = []

    for i in range(count):
        day_offset = start_days_ago if same_day else start_days_ago + i
        txn = Transaction(
            user_id=user_id,
            statement_id=statement.id,
            amount=Decimal(str(random.randint(*amount_range))),
            transaction_type=transaction_type,
            category=category,
            merchant=f"Test Merchant {i}",
            source="manual",
            transaction_date=date.today() - timedelta(days=day_offset),
        )
        db_session.add(txn)
        transactions.append(txn)

    db_session.commit()

    for txn in transactions:
        db_session.refresh(txn)

    return statement, transactions