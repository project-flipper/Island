"""Added email column

Revision ID: 57e919a1bb46
Revises: 
Create Date: 2020-10-21 13:19:47.399562

"""
from alembic import op
import sqlalchemy as sa
import citext


# revision identifiers, used by Alembic.
revision = "57e919a1bb46"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    conn.execute(sa.sql.text("CREATE EXTENSION IF NOT EXISTS citext;"))

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=12), nullable=False),
        sa.Column("nickname", sa.String(length=20), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("email", citext.CIText(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")

    conn = op.get_bind()
    conn.execute(sa.sql.text("DROP EXTENSION IF EXISTS citext;"))
    # ### end Alembic commands ###
