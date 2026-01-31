"""Merge heads: da49d84f064b and 0001_rename_timestamp_to_measured_at

Revision ID: 0002_merge_heads_da49_and_0001
Revises: da49d84f064b, 0001_rename_timestamp_to_measured_at
Create Date: 2026-01-30 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_merge_heads_da49_and_0001'
down_revision = ('da49d84f064b', '0001_rename_ts')
branch_labels = None
depends_on = None


def upgrade():
    # Merge-only revision; no schema changes.
    pass


def downgrade():
    # No downgrade; this is a merge marker only.
    pass
