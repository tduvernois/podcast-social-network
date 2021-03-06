"""comments

Revision ID: f80f99a150e0
Revises: dd4c3d420cf0
Create Date: 2020-10-08 00:16:02.750279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f80f99a150e0'
down_revision = 'dd4c3d420cf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.String(length=5000), nullable=True))
        batch_op.drop_column('comment')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.VARCHAR(length=5000), nullable=True))
        batch_op.drop_column('message')

    # ### end Alembic commands ###
