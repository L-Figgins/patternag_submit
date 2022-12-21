"""resource column

Revision ID: 9310efe03f97
Revises: e1480d1b98d1
Create Date: 2022-12-20 09:58:44.135688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9310efe03f97"
down_revision = "e1480d1b98d1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("jobs", sa.Column("resource_id", sa.String(50)))


def downgrade() -> None:
    op.drop_column("jobs", sa.Column("resource_id", sa.String(50)))
