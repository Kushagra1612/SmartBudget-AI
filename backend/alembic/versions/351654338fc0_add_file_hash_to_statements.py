"""add file_hash to statements

Revision ID: 351654338fc0
Revises: 9efdd73308bb
Create Date: 2026-08-24 10:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "351654338fc0"
down_revision: Union[str, Sequence[str], None] = "9efdd73308bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "statements",
        sa.Column("file_hash", sa.String(length=64), nullable=True),
    )
    # Unique per user, not globally -- two different users legitimately
    # uploading the same sample/demo PDF shouldn't collide with each
    # other. NULL file_hash values (pre-existing rows) are exempt from
    # this constraint, which is standard unique-index behavior.
    op.create_index(
        "ix_statements_user_id_file_hash",
        "statements",
        ["user_id", "file_hash"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_statements_user_id_file_hash",
        table_name="statements",
    )
    op.drop_column("statements", "file_hash")
