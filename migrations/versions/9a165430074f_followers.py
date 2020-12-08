"""followers

Revision ID: 9a165430074f
Revises: be287f2ffb6e
Create Date: 2020-10-27 12:09:05.969061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a165430074f'
down_revision = 'be287f2ffb6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], name=op.f('fk_followers_followed_id_user')),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name=op.f('fk_followers_follower_id_user'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
