"""empty message

Revision ID: 02ed474a4ece
Revises: 021a07a92cd0
Create Date: 2021-02-03 20:02:20.029896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02ed474a4ece'
down_revision = '021a07a92cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=120), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###