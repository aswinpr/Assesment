"""add answer_key to tests

Revision ID: 6d852de5460a
Revises: 027860447804
Create Date: 2026-02-12
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '6d852de5460a'
down_revision = '027860447804'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('tests', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'answer_key',
                postgresql.JSONB(astext_type=sa.Text()),
                nullable=True,
                server_default=sa.text("'{}'::jsonb")
            )
        )


def downgrade():
    with op.batch_alter_table('tests', schema=None) as batch_op:
        batch_op.drop_column('answer_key')
