"""Add NOT NULL constraints to inbody_metrics columns

Revision ID: 0003_not_null
Revises: 0002_merge_heads_da49_and_0001
Create Date: 2026-01-31 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_not_null'
down_revision = '0002_merge_heads_da49_and_0001'
branch_labels = None
depends_on = None


def upgrade():
    # Add NOT NULL constraints to inbody_metrics columns
    op.alter_column('inbody_metrics', 'measured_at', existing_type=sa.TIMESTAMP(timezone=True), nullable=False)
    op.alter_column('inbody_metrics', 'weight_lb', existing_type=sa.FLOAT(), nullable=False)
    op.alter_column('inbody_metrics', 'inbody_score', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('inbody_metrics', 'skeletal_muscle_lb', existing_type=sa.FLOAT(), nullable=False)
    op.alter_column('inbody_metrics', 'body_fat_lb', existing_type=sa.FLOAT(), nullable=False)
    op.alter_column('inbody_metrics', 'body_fat_percent', existing_type=sa.FLOAT(), nullable=False)
    op.alter_column('inbody_metrics', 'waist_hip_ratio', existing_type=sa.FLOAT(), nullable=False)
    op.alter_column('inbody_metrics', 'visceral_fat_level', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('inbody_metrics', 'bmr_kcal', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('inbody_metrics', 'soft_lean_lb', existing_type=sa.FLOAT(), nullable=False)


def downgrade():
    # Revert to nullable columns
    op.alter_column('inbody_metrics', 'measured_at', existing_type=sa.TIMESTAMP(timezone=True), nullable=True)
    op.alter_column('inbody_metrics', 'weight_lb', existing_type=sa.FLOAT(), nullable=True)
    op.alter_column('inbody_metrics', 'inbody_score', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('inbody_metrics', 'skeletal_muscle_lb', existing_type=sa.FLOAT(), nullable=True)
    op.alter_column('inbody_metrics', 'body_fat_lb', existing_type=sa.FLOAT(), nullable=True)
    op.alter_column('inbody_metrics', 'body_fat_percent', existing_type=sa.FLOAT(), nullable=True)
    op.alter_column('inbody_metrics', 'waist_hip_ratio', existing_type=sa.FLOAT(), nullable=True)
    op.alter_column('inbody_metrics', 'visceral_fat_level', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('inbody_metrics', 'bmr_kcal', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('inbody_metrics', 'soft_lean_lb', existing_type=sa.FLOAT(), nullable=True)
