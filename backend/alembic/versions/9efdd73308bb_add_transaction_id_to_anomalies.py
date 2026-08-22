"""add transaction_id to anomalies

Revision ID: 9efdd73308bb
Revises: e5dd8e5cda57
Create Date: 2026-08-14 09:29:57.534407

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9efdd73308bb"
down_revision: Union[str, Sequence[str], None] = "e5dd8e5cda57"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "anomalies",
        sa.Column("transaction_id", sa.UUID(), nullable=False),
    )
    op.create_index(
        "ix_anomalies_transaction_id",
        "anomalies",
        ["transaction_id"],
        unique=True,
    )
    op.create_foreign_key(
        "fk_anomalies_transaction_id_transactions",
        "anomalies",
        "transactions",
        ["transaction_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_anomalies_transaction_id_transactions",
        "anomalies",
        type_="foreignkey",
    )
    op.drop_index(
        "ix_anomalies_transaction_id",
        table_name="anomalies",
    )
    op.drop_column("anomalies", "transaction_id")
