"""add duplicate_of_attempt_id

Revision ID: 42fdcc972e63
Revises: d6302f35abbb
Create Date: 2026-02-11 22:50:55.405658
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '42fdcc972e63'
down_revision = 'd6302f35abbb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("attempts") as batch_op:
        # 1. Add column as nullable first
        batch_op.add_column(sa.Column("source_event_id", sa.String(), nullable=True))

    # 2. Backfill existing rows
    op.execute("""
        UPDATE attempts
        SET source_event_id = id::text
        WHERE source_event_id IS NULL
    """)

    # 3. Enforce NOT NULL after backfill
    with op.batch_alter_table("attempts") as batch_op:
        batch_op.alter_column("source_event_id", nullable=False)



def downgrade():
    with op.batch_alter_table("attempts") as batch_op:
        batch_op.drop_column("source_event_id")

