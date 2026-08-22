"""
Isolation Forest anomaly-detection model: training and inference. (Phase 7)

Design notes (read before changing thresholds):

- No model is persisted to disk. Detection re-fits a fresh IsolationForest
  on the user's own expense history every time it runs, so it always
  reflects their latest transactions and there's no stale-model /
  versioning problem to manage. The trade-off is a bit of repeated
  compute per call, which is fine at this data scale.
- Only EXPENSE transactions are considered -- income and transfers aren't
  "spending" and shouldn't be flagged as unusual spending.
- Detection is per-user: what's a normal amount for one person's
  "Entertainment" category may be an outlier for another's, so each
  user's model only ever sees their own transactions.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Protocol, runtime_checkable
from uuid import UUID

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

# Below this many expense transactions, IsolationForest doesn't have enough
# signal to be meaningful -- a handful of points look "unusual" relative to
# each other no matter what. Callers should check this before showing
# results as a confident feature rather than noise.
MIN_TRANSACTIONS_FOR_DETECTION = 15

# Expected fraction of a user's expenses that are genuinely unusual.
# 0.05 = flag roughly the most extreme 5%. Tune this, not the model
# internals, if detection feels too noisy or too quiet in practice.
DEFAULT_CONTAMINATION = 0.05

# Below this z-score, we don't have a confident amount-based story for
# *why* a transaction was flagged, so the explanation falls back to a
# more general one instead of overclaiming precision.
NOTABLE_ZSCORE = 1.5


@runtime_checkable
class TransactionLike(Protocol):
    """
    Structural type for whatever gets passed to detect().

    Real callers pass SQLAlchemy Transaction ORM objects. Tests can pass
    anything with these attributes (a dataclass, a SimpleNamespace, etc.)
    without needing a database.
    """

    id: UUID
    amount: Decimal | float
    category: object  # TransactionCategory enum member (uses .value)
    transaction_type: object  # TransactionType enum member (uses .value)
    transaction_date: date


@dataclass
class AnomalyResult:
    transaction_id: UUID
    amount: float
    category: str
    confidence_score: float  # 0-100, higher = more anomalous
    reason: str


def _to_frame(transactions: list[TransactionLike]) -> pd.DataFrame:
    """Pull out the raw fields we need into a flat DataFrame."""

    rows = []

    for txn in transactions:
        rows.append(
            {
                "transaction_id": txn.id,
                "amount": float(txn.amount),
                "category": txn.category.value,
                "day_of_week": txn.transaction_date.weekday(),
                "day_of_month": txn.transaction_date.day,
            }
        )

    return pd.DataFrame(rows)


def _add_zscores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add two deviation signals:

    - category_zscore: how unusual the amount is for *this category*,
      relative to the user's own history in that category.
    - overall_zscore: how unusual the amount is relative to the user's
      overall transaction sizes, regardless of category.

    A category with only one or two prior transactions doesn't have a
    meaningful average to compare against (the "average" is just the
    transaction itself), so category_zscore alone would miss a genuinely
    large first-time purchase in a rarely-used category. overall_zscore
    is the fallback signal for exactly that case.
    """

    stats = df.groupby("category")["amount"].agg(["mean", "std"]).rename(
        columns={"mean": "category_mean", "std": "category_std"}
    )
    df = df.merge(stats, on="category", how="left")

    fallback_std = (df["category_mean"] * 0.5).replace(0, 1.0)
    needs_fallback = df["category_std"].isna() | (df["category_std"] == 0)
    df["category_std"] = df["category_std"].mask(needs_fallback, fallback_std)
    df["category_zscore"] = (df["amount"] - df["category_mean"]) / df["category_std"]

    overall_mean = df["amount"].mean()
    overall_std = df["amount"].std() or (overall_mean * 0.5) or 1.0
    df["overall_mean"] = overall_mean
    df["overall_zscore"] = (df["amount"] - overall_mean) / overall_std

    return df


def _build_features(df: pd.DataFrame) -> pd.DataFrame:
    category_dummies = pd.get_dummies(df["category"], prefix="cat")

    features = pd.concat(
        [
            df[
                [
                    "amount",
                    "day_of_week",
                    "day_of_month",
                    "category_zscore",
                    "overall_zscore",
                ]
            ],
            category_dummies,
        ],
        axis=1,
    )

    return features


def _explain(row: pd.Series) -> str:
    amount = row["amount"]
    category = row["category"]

    cat_z = row["category_zscore"]
    cat_avg = row["category_mean"]

    if abs(cat_z) >= NOTABLE_ZSCORE and cat_avg > 0:
        ratio = amount / cat_avg
        direction = "higher" if amount > cat_avg else "lower"
        return (
            f"This ₹{amount:,.2f} {category} transaction is {ratio:.1f}x your "
            f"typical {category} spend (avg ₹{cat_avg:,.2f}) -- notably "
            f"{direction} than usual."
        )

    overall_z = row["overall_zscore"]
    overall_avg = row["overall_mean"]

    if abs(overall_z) >= NOTABLE_ZSCORE and overall_avg > 0:
        ratio = amount / overall_avg
        return (
            f"This ₹{amount:,.2f} {category} transaction is {ratio:.1f}x the "
            f"size of your typical transaction overall (avg ₹{overall_avg:,.2f}) "
            f"-- {category} doesn't have enough history yet for a "
            f"category-specific comparison."
        )

    return (
        f"This ₹{amount:,.2f} {category} transaction doesn't match your usual "
        f"spending pattern (timing and amount combined look unusual, even "
        f"though the amount alone isn't extreme)."
    )


def detect(
    transactions: list[TransactionLike],
    *,
    contamination: float = DEFAULT_CONTAMINATION,
    random_state: int = 42,
) -> list[AnomalyResult]:
    """
    Score a user's expense transactions and return the ones flagged as
    anomalous. Returns [] if there isn't enough data yet -- callers should
    check len(expenses) against MIN_TRANSACTIONS_FOR_DETECTION themselves
    if they need to tell "not enough data" apart from "nothing unusual".
    """

    expenses = [
        txn for txn in transactions if txn.transaction_type.value == "Expense"
    ]

    if len(expenses) < MIN_TRANSACTIONS_FOR_DETECTION:
        return []

    df = _to_frame(expenses)
    df = _add_zscores(df)
    features = _build_features(df)

    model = IsolationForest(
        contamination=contamination,
        n_estimators=200,
        random_state=random_state,
    )
    predictions = model.fit_predict(features)  # -1 = outlier, 1 = inlier
    raw_scores = model.decision_function(features)  # higher = more normal

    anomaly_scores = -raw_scores  # higher = more anomalous, easier to reason about

    # Min-max normalize to a 0-100 "confidence" scale for display. Guard
    # against a degenerate all-equal-score batch (constant / zero range).
    score_range = anomaly_scores.max() - anomaly_scores.min()
    if score_range > 0:
        normalized = (anomaly_scores - anomaly_scores.min()) / score_range * 100
    else:
        normalized = np.zeros_like(anomaly_scores)

    df["is_anomaly"] = predictions == -1
    df["confidence_score"] = normalized

    results = []

    for _, row in df[df["is_anomaly"]].iterrows():
        results.append(
            AnomalyResult(
                transaction_id=row["transaction_id"],
                amount=round(float(row["amount"]), 2),
                category=row["category"],
                confidence_score=round(float(row["confidence_score"]), 2),
                reason=_explain(row),
            )
        )

    # Highest confidence first -- most-anomalous transactions lead.
    results.sort(key=lambda r: r.confidence_score, reverse=True)

    return results
