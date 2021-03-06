"""image and audio link

Revision ID: b109364f45b4
Revises: 56a5790929a1
Create Date: 2020-09-12 17:38:04.338768

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b109364f45b4'
down_revision = '56a5790929a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('episode', sa.Column('audio_link', sa.String(length=500), nullable=True))
    op.add_column('podcast', sa.Column('image', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('podcast', 'image')
    op.drop_column('episode', 'audio_link')
    # ### end Alembic commands ###
