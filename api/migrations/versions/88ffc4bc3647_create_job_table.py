"""create job table

Revision ID: 88ffc4bc3647
Revises: 
Create Date: 2022-12-19 00:47:33.035949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "88ffc4bc3647"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
    )


def downgrade() -> None:
    op.drop_table("jobs")
