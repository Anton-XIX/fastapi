"""Added expiration date for token model
Revision ID: d6d7e9ae27b7
Revises: 00087e6d1965
Create Date: 2022-04-16 10:07:27.143095
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'd6d7e9ae27b7'
down_revision = '00087e6d1965'
branch_labels = None
depends_on = None
def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('expiration_date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###
def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('token', 'expiration_date')
    # ### end Alembic commands ###