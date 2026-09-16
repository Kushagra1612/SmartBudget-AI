"""add grocery to transactioncategory enum

Revision ID: a7c3f19d2e6b
Revises: bedbc28c2af6
Create Date: 2026-09-06 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a7c3f19d2e6b"
down_revision: Union[str, Sequence[str], None] = "bedbc28c2af6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Postgres allows adding a new value to an existing enum type
    # in-place. On Postgres 12+, this is safe inside a normal
    # transaction as long as the new value isn't USED in that same
    # transaction (we're only adding it here, not inserting rows with
    # it), so no special transaction handling is needed.
    #
    # NOTE: this assumes the Postgres enum type is named
    # "transactioncategory" -- SQLAlchemy's default naming for
    # sa.Enum(SomePythonEnum) when no explicit name= is given. If your
    # actual type has a different name, check with:
    #   psql> \dT
    # and adjust the type name below to match.
    op.execute(
        "ALTER TYPE transactioncategory ADD VALUE IF NOT EXISTS 'Grocery'"
    )


def downgrade() -> None:
    # Postgres has no "DROP VALUE" for enum types -- removing one
    # requires rebuilding the type from scratch: create a new enum
    # without it, repoint the column to the new type, drop the old
    # type, rename the new one into place. Any existing rows using
    # 'Grocery' are remapped to 'Other' first so nothing is left
    # referencing a value that's about to disappear.
    op.execute(
        "UPDATE transactions SET category = 'Other' "
        "WHERE category = 'Grocery'"
    )

    op.execute(
        "ALTER TYPE transactioncategory RENAME TO transactioncategory_old"
    )

    op.execute(
        "CREATE TYPE transactioncategory AS ENUM ("
        "'Food', 'Shopping', 'Transport', 'Health', 'Entertainment', "
        "'Utilities', 'Education', 'Salary', 'Investment', 'Other'"
        ")"
    )

    op.execute(
        "ALTER TABLE transactions "
        "ALTER COLUMN category TYPE transactioncategory "
        "USING category::text::transactioncategory"
    )

    op.execute("DROP TYPE transactioncategory_old")