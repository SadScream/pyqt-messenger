"""Date added

Revision ID: 24763aef4f73
Revises: a40e26a1083f
Create Date: 2022-02-08 21:28:42.715162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24763aef4f73'
down_revision = 'a40e26a1083f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('date', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('message', 'date')
    # ### end Alembic commands ###
