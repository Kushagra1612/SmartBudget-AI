"""remove is_deleted from budgets

Revision ID: e5dd8e5cda57
Revises: 6f1d95c35a49
Create Date: 2026-08-06 01:25:49.875469

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5dd8e5cda57"
down_revision: Union[str, Sequence[str], None] = "6f1d95c35a49"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("budgets", "is_deleted")


def downgrade() -> None:
    op.add_column(
        "budgets",
        sa.Column(
            "is_deleted",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )