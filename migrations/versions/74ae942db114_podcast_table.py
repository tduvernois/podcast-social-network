"""podcast table

Revision ID: 74ae942db114
Revises: a8cde2884488
Create Date: 2020-09-04 23:20:33.131078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74ae942db114'
down_revision = 'a8cde2884488'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('podcast',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_podcast_timestamp'), 'podcast', ['timestamp'], unique=False)
    op.create_table('UserPodcast',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('podcast_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['podcast_id'], ['podcast.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'podcast_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('UserPodcast')
    op.drop_index(op.f('ix_podcast_timestamp'), table_name='podcast')
    op.drop_table('podcast')
    # ### end Alembic commands ###
