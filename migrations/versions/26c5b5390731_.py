"""empty message

Revision ID: 26c5b5390731
Revises: 
Create Date: 2020-12-21 14:42:59.812234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26c5b5390731'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('password1', sa.String(length=180), nullable=True))
    op.drop_column('customer', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('password', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('customer', 'password1')
    # ### end Alembic commands ###
