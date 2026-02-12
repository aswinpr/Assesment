"""convert negative_marking to float

Revision ID: 8f951708f9c4
Revises: dec157e99688
Create Date: 2026-02-12 10:10:04.866170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f951708f9c4'
down_revision = 'dec157e99688'
branch_labels = None
depends_on = None


def upgrade():
    # Convert JSONB → FLOAT explicitly
    op.execute("""
        ALTER TABLE tests
        ALTER COLUMN negative_marking
        TYPE DOUBLE PRECISION
        USING (
            CASE
                WHEN jsonb_typeof(negative_marking) = 'object'
                THEN (negative_marking->>'per_question')::double precision
                ELSE negative_marking::text::double precision
            END
        )
    """)


def downgrade():
    op.execute("""
        ALTER TABLE tests
        ALTER COLUMN negative_marking
        TYPE JSONB
        USING to_jsonb(negative_marking)
    """)


    # ### end Alembic commands ###
