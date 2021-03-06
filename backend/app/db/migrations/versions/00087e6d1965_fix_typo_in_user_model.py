"""fix typo in user model
Revision ID: 00087e6d1965
Revises: e6f511e1767f
Create Date: 2022-04-06 18:10:10.271671
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic
revision = "00087e6d1965"
down_revision = "e6f511e1767f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False)
    )
    op.drop_index("ix_user_uid", table_name="user")
    op.create_index(op.f("ix_user_uuid"), "user", ["uuid"], unique=False)
    op.drop_column("user", "uid")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user", sa.Column("uid", postgresql.UUID(), autoincrement=False, nullable=False)
    )
    op.drop_index(op.f("ix_user_uuid"), table_name="user")
    op.create_index("ix_user_uid", "user", ["uid"], unique=False)
    op.drop_column("user", "uuid")
    # ### end Alembic commands ###
