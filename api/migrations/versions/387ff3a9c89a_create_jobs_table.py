"""create jobs table

Revision ID: 387ff3a9c89a
Revises: 
Create Date: 2022-12-20 18:38:39.719644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "387ff3a9c89a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "jobs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50)),
        sa.Column("timestamp", sa.Integer),
        sa.Column("resource_id", sa.String(50)),
        sa.Column("status", sa.String(10)),
    )


def downgrade() -> None:
    op.drop_table("jobs")
