"""Первоначальная схема аптеки.
Revision ID: 001
Revises:
"""
from alembic import op
from app.models import Base

revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind)


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind)
