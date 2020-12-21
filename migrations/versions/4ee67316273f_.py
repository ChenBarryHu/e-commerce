"""empty message

Revision ID: 4ee67316273f
Revises: 26c5b5390731
Create Date: 2020-12-21 14:43:55.804642

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ee67316273f'
down_revision = '26c5b5390731'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('password', sa.String(length=180), nullable=True))
    op.drop_column('customer', 'password1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('password1', sa.VARCHAR(length=180), autoincrement=False, nullable=True))
    op.drop_column('customer', 'password')
    # ### end Alembic commands ###
