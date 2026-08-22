"""
Unit tests for app/ml/anomaly_detector.py. Pure logic -- no database, no
FastAPI app. Uses plain dataclass stand-ins instead of real ORM objects
since the detector only needs attribute access, not a live session.

This is the real version of the earlier smoke_test_detector.py script
(kept for reference in the repo root) -- same idea, as pytest tests.
"""

import random
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from app.ml.anomaly_detector import MIN_TRANSACTIONS_FOR_DETECTION, detect
from app.models.transaction import TransactionCategory, TransactionType


@dataclass
class FakeTransaction:
    id: object
    amount: Decimal
    category: TransactionCategory
    transaction_type: TransactionType
    transaction_date: date


@pytest.fixture(autouse=True)
def _seeded_random():
    # Deterministic test data -- IsolationForest itself is already
    # seeded via random_state inside detect(), this seeds the *data
    # generation* so re-runs are reproducible too.
    random.seed(7)


def _normal_transactions(
    count,
    category,
    amount_range,
    transaction_type=TransactionType.EXPENSE,
    start_days_ago=1,
):
    today = date.today()

    return [
        FakeTransaction(
            id=uuid4(),
            amount=Decimal(str(random.randint(*amount_range))),
            category=category,
            transaction_type=transaction_type,
            transaction_date=today - timedelta(days=start_days_ago + i),
        )
        for i in range(count)
    ]


def test_returns_nothing_below_the_minimum_transaction_count():
    txns = _normal_transactions(
        MIN_TRANSACTIONS_FOR_DETECTION - 1,
        TransactionCategory.FOOD,
        (300, 600),
    )

    assert detect(txns) == []


def test_flags_a_large_outlier_transaction():
    txns = _normal_transactions(25, TransactionCategory.FOOD, (300, 600))

    outlier_id = uuid4()
    txns.append(
        FakeTransaction(
            id=outlier_id,
            amount=Decimal("18500"),
            category=TransactionCategory.FOOD,
            transaction_type=TransactionType.EXPENSE,
            transaction_date=date.today() - timedelta(days=5),
        )
    )

    results = detect(txns)
    flagged_ids = {r.transaction_id for r in results}

    assert outlier_id in flagged_ids


def test_does_not_flag_ordinary_transactions():
    txns = _normal_transactions(30, TransactionCategory.FOOD, (300, 600))

    results = detect(txns)

    # contamination=0.05 on 30 unremarkable, similar-looking transactions
    # should flag at most one or two by chance, not a large chunk of them.
    assert len(results) <= 2


def test_never_flags_income_or_transfers():
    txns = _normal_transactions(20, TransactionCategory.FOOD, (300, 600))

    income_id = uuid4()
    txns.append(
        FakeTransaction(
            id=income_id,
            amount=Decimal("999999"),  # huge, but it's income, not spending
            category=TransactionCategory.SALARY,
            transaction_type=TransactionType.INCOME,
            transaction_date=date.today(),
        )
    )

    results = detect(txns)
    flagged_ids = {r.transaction_id for r in results}

    assert income_id not in flagged_ids


def test_confidence_scores_stay_within_0_to_100():
    txns = _normal_transactions(25, TransactionCategory.FOOD, (300, 600))
    txns += _normal_transactions(
        5,
        TransactionCategory.SHOPPING,
        (8000, 9000),
        start_days_ago=30,
    )

    results = detect(txns)

    assert all(0 <= r.confidence_score <= 100 for r in results)


def test_results_are_sorted_most_anomalous_first():
    txns = _normal_transactions(30, TransactionCategory.FOOD, (300, 600))
    txns.append(
        FakeTransaction(
            id=uuid4(),
            amount=Decimal("20000"),
            category=TransactionCategory.FOOD,
            transaction_type=TransactionType.EXPENSE,
            transaction_date=date.today() - timedelta(days=2),
        )
    )

    results = detect(txns)
    scores = [r.confidence_score for r in results]

    assert scores == sorted(scores, reverse=True)


def test_a_first_ever_purchase_in_a_new_category_can_still_be_flagged():
    # Regression check for the sparse-category case found while building
    # this: a category with only one transaction has no meaningful
    # category average to compare against, so detection has to fall
    # back to an overall-spending comparison instead of silently missing
    # a genuinely large one-off purchase.
    txns = _normal_transactions(25, TransactionCategory.FOOD, (300, 600))

    first_shopping_id = uuid4()
    txns.append(
        FakeTransaction(
            id=first_shopping_id,
            amount=Decimal("9200"),
            category=TransactionCategory.SHOPPING,
            transaction_type=TransactionType.EXPENSE,
            transaction_date=date.today() - timedelta(days=12),
        )
    )

    results = detect(txns)
    flagged_ids = {r.transaction_id for r in results}

    assert first_shopping_id in flagged_ids
