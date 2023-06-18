"""add ban, user, and world tables

Revision ID: 78624ea61cdb
Revises: 
Create Date: 2023-06-18 21:16:05.430016

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlalchemy_utils

# revision identifiers, used by Alembic.
revision = '78624ea61cdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=12), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('email', sqlalchemy_utils.types.encrypted.encrypted_type.StringEncryptedType(), nullable=False),
    sa.Column('created_timestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_timestamp', sa.DateTime(), nullable=True),
    sa.Column('scopes', sa.ARRAY(sa.String(length=30)), server_default='{}', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('worlds',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('lang', sa.Integer(), nullable=False),
    sa.Column('is_safe', sa.Boolean(), nullable=False),
    sa.Column('access_key', sa.String(length=32), nullable=False),
    sa.Column('grant_scopes', postgresql.ARRAY(sa.String(length=30)), server_default='{}', nullable=False),
    sa.Column('scopes', postgresql.ARRAY(sa.String(length=30)), server_default='{}', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('access_key'),
    sa.UniqueConstraint('name')
    )
    op.create_table('bans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('ban_type', sa.Enum('MANUAL_BAN', 'AUTO_BAN', 'CHEATING_BAN', name='bantype'), nullable=False),
    sa.Column('ban_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('ban_expire', sa.DateTime(), nullable=False),
    sa.Column('ban_user', sa.Integer(), nullable=False),
    sa.Column('ban_comment', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bans')
    op.drop_table('worlds')
    op.drop_table('users')
    # ### end Alembic commands ###
