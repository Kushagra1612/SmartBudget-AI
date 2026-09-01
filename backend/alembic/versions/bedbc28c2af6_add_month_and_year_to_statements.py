from alembic import op
import sqlalchemy as sa

revision = "bedbc28c2af6"
down_revision = "351654338fc0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "statements",
        sa.Column("month", sa.Integer(), nullable=True)
    )

    op.add_column(
        "statements",
        sa.Column("year", sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("statements", "year")
    op.drop_column("statements", "month")