"""tables nicknamehistory and connectionhistory merged with table messages

Revision ID: 208efaf6f3d9
Revises: b935ed8aae6b
Create Date: 2022-03-07 18:20:06.794220

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '208efaf6f3d9'
down_revision = 'b935ed8aae6b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('message', sa.Column('msg_type', sa.Enum('NEW_MESSAGE', 'CONNECTION', 'DISCONNECTION', 'NAME_CHANGED', name='messagetypes'), nullable=False))
    op.add_column('message', sa.Column('old_username', sa.String(length=36), nullable=True))
    op.add_column('message', sa.Column('new_username', sa.String(length=36), nullable=True))
    op.alter_column('message', 'text',
               existing_type=mysql.VARCHAR(length=1024),
               nullable=True)
    op.drop_constraint('message_ibfk_1', 'message', type_='foreignkey')
    op.create_foreign_key(None, 'message', 'user', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_column('message', 'owner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('message', sa.Column('owner_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'message', type_='foreignkey')
    op.create_foreign_key('message_ibfk_1', 'message', 'user', ['owner_id'], ['user_id'], ondelete='CASCADE')
    op.alter_column('message', 'text',
               existing_type=mysql.VARCHAR(length=1024),
               nullable=False)
    op.drop_column('message', 'new_username')
    op.drop_column('message', 'old_username')
    op.drop_column('message', 'msg_type')
    op.drop_column('message', 'user_id')
    # ### end Alembic commands ###