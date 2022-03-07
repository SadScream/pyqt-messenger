"""datetime to datetime(fsp=6)

Revision ID: b935ed8aae6b
Revises: a5b7dbbd275b
Create Date: 2022-03-07 16:17:26.230286

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import DATETIME


# revision identifiers, used by Alembic.
revision = 'b935ed8aae6b'
down_revision = 'a5b7dbbd275b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('message', 'date',
               existing_type=sa.DateTime(),
               type_=DATETIME(fsp=6),
               existing_nullable=False)
    op.alter_column('connectionhistory', 'date',
               existing_type=sa.DateTime(),
               type_=DATETIME(fsp=6),
               existing_nullable=False)
    op.alter_column('usernamehistory', 'date',
               existing_type=sa.DateTime(),
               type_=DATETIME(fsp=6),
               existing_nullable=False)


def downgrade():
    op.alter_column('message', 'date',
               existing_type=DATETIME(fsp=6),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.alter_column('connectionhistory', 'date',
               existing_type=DATETIME(fsp=6),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.alter_column('usernamehistory', 'date',
               existing_type=DATETIME(fsp=6),
               type_=sa.DateTime(),
               existing_nullable=False)
