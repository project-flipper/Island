"""Added scopes

Revision ID: 93ef17250727
Revises: 57e919a1bb46
Create Date: 2020-10-23 17:02:07.658792

"""
from alembic import op
import sqlalchemy as sa
import citext


# revision identifiers, used by Alembic.
revision = '93ef17250727'
down_revision = '57e919a1bb46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scopes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag', citext.CIText(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['scopes.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag')
    )
    op.create_table('user_scopes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('scope_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['scope_id'], ['scopes.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE')
    )
    meta = sa.MetaData(bind=op.get_bind())
    scopes = sa.Table('scopes', meta,autoload=True)
    op.bulk_insert(scopes, [{"id":0,"tag":"master","description":"master access","group_id":None},{"id":1,"tag":"read","description":"allow read access","group_id":0},{"id":2,"tag":"write","description":"allow write/mutate/modify access","group_id":0},{"id":3,"tag":"create","description":"allow create access","group_id":0},{"id":4,"tag":"user:read","description":"allow read user data","group_id":1},{"id":5,"tag":"user:write","description":"allow write user data","group_id":2},{"id":6,"tag":"user:create","description":"allow create user data","group_id":3}])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_scopes')
    op.drop_table('scopes')
    # ### end Alembic commands ###
