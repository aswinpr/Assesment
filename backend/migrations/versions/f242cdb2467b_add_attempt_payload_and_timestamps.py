from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "xxxx"
down_revision = "42fdcc972e63"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("attempts") as batch_op:
        batch_op.add_column(sa.Column("started_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column("answers", postgresql.JSONB(), nullable=True))
        batch_op.add_column(sa.Column("raw_payload", postgresql.JSONB(), nullable=True))

    # Backfill required fields for existing rows
    op.execute("""
        UPDATE attempts
        SET
            started_at = NOW(),
            answers = '{}'::jsonb,
            raw_payload = '{}'::jsonb
        WHERE started_at IS NULL
    """)

    # Enforce NOT NULL where required
    with op.batch_alter_table("attempts") as batch_op:
        batch_op.alter_column("started_at", nullable=False)
        batch_op.alter_column("answers", nullable=False)
        batch_op.alter_column("raw_payload", nullable=False)


def downgrade():
    with op.batch_alter_table("attempts") as batch_op:
        batch_op.drop_column("raw_payload")
        batch_op.drop_column("answers")
        batch_op.drop_column("submitted_at")
        batch_op.drop_column("started_at")
