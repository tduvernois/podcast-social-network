"""empty message

Revision ID: 8c0c6a747cb2
Revises: dad77bf8c832
Create Date: 2020-09-21 22:43:14.640279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c0c6a747cb2'
down_revision = 'dad77bf8c832'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'podcast', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'podcast', type_='foreignkey')
    # ### end Alembic commands ###
