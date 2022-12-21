"""Add resource_id column

Revision ID: e1480d1b98d1
Revises: dfc09e0fe64d
Create Date: 2022-12-20 09:31:22.843845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1480d1b98d1'
down_revision = 'dfc09e0fe64d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('jobs', sa.Column('resource_id', sa.String(50)))


def downgrade() -> None:
    op.drop_column('jobs', sa.Column('resource_id', sa.String(50)))

