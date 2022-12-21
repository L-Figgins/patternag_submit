"""add sample table

Revision ID: 705090cbe870
Revises: 9310efe03f97
Create Date: 2022-12-20 13:14:06.213883

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "705090cbe870"
down_revision = "9310efe03f97"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "samples",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("sample_id", sa.String(36)),
        sa.Column("kegg_ortholog", sa.String(6)),
        sa.Column("lineage_rank", sa.String),
        sa.Column("read_count", sa.Integer),
        sa.Column("relative_abundance", sa.String),
        sa.Column("total_filtered_reads", sa.Integer),
        sa.Column("rank", sa.String(15)),
        sa.Column("taxon_name", sa.String(50)),
    )


def downgrade() -> None:
    op.drop_table("samples")
