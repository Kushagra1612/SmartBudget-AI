"""add correctly-cased GROCERY to transactioncategory enum

Revision ID: f2d84a1c9b77
Revises: a7c3f19d2e6b
Create Date: 2026-09-06 20:15:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f2d84a1c9b77"
down_revision: Union[str, Sequence[str], None] = "a7c3f19d2e6b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The previous migration (a7c3f19d2e6b) added 'Grocery'
    # (capitalized, matching the Python enum's VALUE). But
    # SQLAlchemy's Enum(SomePythonEnum) column type serializes by
    # the member's NAME by default (not its value) unless
    # values_callable is explicitly configured -- and every existing
    # category in this table is already stored uppercase (FOOD,
    # OTHER, UTILITIES, etc.), confirming that's the convention
    # actually in use here.
    #
    # So the previous migration added the wrong casing. This adds
    # the correct one. The old 'Grocery' label is left in place as
    # a harmless, unused extra -- Postgres enum types don't support
    # removing individual values without a full type rebuild, and
    # it costs nothing to leave it.
    op.execute(
        "ALTER TYPE transactioncategory ADD VALUE IF NOT EXISTS 'GROCERY'"
    )


def downgrade() -> None:
    # Rebuild the type without GROCERY (and without the stray
    # mixed-case 'Grocery' from the previous migration too, cleaning
    # up both at once). Any rows using either are remapped to OTHER
    # first.
    op.execute(
        "UPDATE transactions SET category = 'OTHER' "
        "WHERE category IN ('GROCERY', 'Grocery')"
    )

    op.execute(
        "ALTER TYPE transactioncategory RENAME TO transactioncategory_old"
    )

    op.execute(
        "CREATE TYPE transactioncategory AS ENUM ("
        "'FOOD', 'SHOPPING', 'TRANSPORT', 'HEALTH', 'ENTERTAINMENT', "
        "'UTILITIES', 'EDUCATION', 'SALARY', 'INVESTMENT', 'OTHER'"
        ")"
    )

    op.execute(
        "ALTER TABLE transactions "
        "ALTER COLUMN category TYPE transactioncategory "
        "USING category::text::transactioncategory"
    )

    op.execute("DROP TYPE transactioncategory_old")
