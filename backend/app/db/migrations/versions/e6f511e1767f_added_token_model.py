"""added token model
Revision ID: e6f511e1767f
Revises: 4fad59946e6d
Create Date: 2022-04-06 17:59:44.734226
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = "e6f511e1767f"
down_revision = "4fad59946e6d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "token",
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=512), nullable=False),
        sa.Column(
            "token_type", sa.Enum("access", "refresh", name="tokentype"), nullable=False
        ),
        sa.Column("user_uuid", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("fresh", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_token_id"), "token", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_token_id"), table_name="token")
    op.drop_table("token")
    # ### end Alembic commands ###
