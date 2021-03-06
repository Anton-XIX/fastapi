"""Added user profiel
Revision ID: 5323e78a61de
Revises: 3fb4cb05ad22
Create Date: 2022-05-01 12:16:31.979630
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
# revision identifiers, used by Alembic
revision = '5323e78a61de'
down_revision = '3fb4cb05ad22'
branch_labels = None
depends_on = None
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userprofile',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=256), nullable=True),
    sa.Column('last_name', sa.String(length=256), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('user_uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_uuid')
    )
    op.create_index(op.f('ix_userprofile_id'), 'userprofile', ['id'], unique=True)
    # ### end Alembic commands ###
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_userprofile_id'), table_name='userprofile')
    op.drop_table('userprofile')
    # ### end Alembic commands ###