"""Add timestamp column and status column

Revision ID: dfc09e0fe64d
Revises: 88ffc4bc3647
Create Date: 2022-12-20 09:18:05.369176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfc09e0fe64d'
down_revision = '88ffc4bc3647'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('jobs', sa.Column('timestamp', sa.Integer))
    op.add_column('jobs', sa.Column('status', sa.String(10)))


def downgrade() -> None:
    op.add_column('jobs', sa.Column('timestamp', sa.Integer))
    op.add_column('jobs', sa.Column('status', sa.String(10)))
