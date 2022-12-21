"""create samples table

Revision ID: a5853d73eb82
Revises: 387ff3a9c89a
Create Date: 2022-12-20 18:46:22.766597

"""
import uuid
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = "a5853d73eb82"
down_revision = "387ff3a9c89a"
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
