"""Rename timestamp to measured_at on inbody_metrics

Revision ID: 0001_rename_timestamp_to_measured_at
Revises: 
Create Date: 2026-01-30 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_rename_ts'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # On Postgres this will rename the column in-place.
    op.alter_column(
        'inbody_metrics',
        'timestamp',
        new_column_name='measured_at',
        existing_type=sa.TIMESTAMP(timezone=True),
    )


def downgrade():
    op.alter_column(
        'inbody_metrics',
        'measured_at',
        new_column_name='timestamp',
        existing_type=sa.TIMESTAMP(timezone=True),
    )
