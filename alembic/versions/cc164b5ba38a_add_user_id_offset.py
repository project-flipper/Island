"""Add user id offset

Revision ID: cc164b5ba38a
Revises: 522958959b6d
Create Date: 2025-03-30 20:16:41.411084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision: str = 'cc164b5ba38a'
down_revision: Union[str, None] = '522958959b6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            SELECT setval('users_id_seq', (SELECT MAX(id) FROM users) + 100);
            """
        )
    )


def downgrade() -> None:
    connection = op.get_bind()
    connection.execute(
        sa.text(
            """
            SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
            """
        )
    )
