"""followers

Revision ID: 8c635889a70f
Revises: 5d4baf36fe39
Create Date: 2020-10-07 23:00:50.228995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c635889a70f'
down_revision = '5d4baf36fe39'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.String(length=5000), nullable=True),
    sa.Column('episode_time', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_comment'))
    )
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_comment_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_comment_timestamp'))

    op.drop_table('comment')
    # ### end Alembic commands ###
