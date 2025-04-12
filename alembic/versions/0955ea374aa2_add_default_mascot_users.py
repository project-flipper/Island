"""Add default mascot users

Revision ID: 0955ea374aa2
Revises: cc164b5ba38a
Create Date: 2025-04-12 15:12:33.218835

"""
from typing import Sequence, Union, Any, List, Tuple
from island.core.config import DATABASE_SECRET_KEY

import sqlalchemy as sa
from alembic import op
from sqlalchemy_utils import StringEncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine


# revision identifiers, used by Alembic.
revision: str = '0955ea374aa2'
down_revision: Union[str, None] = 'cc164b5ba38a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


users_table = sa.table(
    'users',
    sa.column('id', sa.Integer),
    sa.column('username', sa.String(12)),
    sa.column('nickname', sa.String(20)),
    sa.column('password', sa.Text),
    sa.column('email', StringEncryptedType(sa.String, str(DATABASE_SECRET_KEY), AesEngine, "pkcs5")),
    sa.column('scopes', sa.ARRAY(sa.String(length=30))),
    sa.column('avatar_id', sa.Integer),
    sa.column('lang', sa.Integer),
    sa.column('mascot_id', sa.Integer),
    sa.column('created_timestamp', sa.DateTime),
    sa.column('updated_timestamp', sa.DateTime),
)

users_data = (
    (1, 'rockhopper', 'Rockhopper', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (2, 'aunt arctic', 'Aunt Arctic', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (3, 'cadence', 'Cadence', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (4, 'gary', 'Gary', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (5, 'franky', 'Franky', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (6, 'petey k', 'Petey K', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (7, 'g billy', 'G Billy', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (8, 'stompin bob', 'Stompin Bob', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (9, 'sensei', 'Sensei', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (10, 'herbert', 'Herbert P Bear', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (11, 'wheel bot', 'Wheel Bot', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (12, 'jet bot', 'Jet Bot', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (13, 'snow bot', 'Snow Bot', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (14, 'protobot', 'Protobot', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (15, 'dot', 'Dot', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (16, 'rookie', 'Rookie', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (17, 'jet pack guy', 'Jet Pack Guy', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', '', '', None),
    (18, 'director', 'Director', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (19, 'klutzy', 'Klutzy', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (20, 'g', 'G', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (21, 'ph', 'PH', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (22, 'brady', 'Brady', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (23, 'mckenzie', 'McKenzie', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (24, 'kermit', 'Kermit The Frog', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None),
    (25, 'sam', 'Sam', '$2b$12$CCYijGFRZyymIJWWNpkmP.pysAEN5E1mRwPtrjIDmTR3LnhKdJeBK', 'mascot@projectflipper.me', '', None)
)


mascots_table = sa.table(
    'mascots',
    sa.column('id', sa.Integer()),
    sa.column('name', sa.String(length=256)),
    sa.column('title', sa.String(length=256)),
    sa.column('gift_id', sa.Integer()),
    sa.column('created_timestamp', sa.DateTime()),
    sa.column('updated_timestamp', sa.DateTime()),
)

avatars_table = sa.table(
    'avatars',
    sa.column('id', sa.Integer),
    sa.column('color', sa.Integer),
    sa.column('head', sa.Integer),
    sa.column('face', sa.Integer),
    sa.column('neck', sa.Integer),
    sa.column('body', sa.Integer),
    sa.column('hand', sa.Integer),
    sa.column('feet', sa.Integer),
    sa.column('photo', sa.Integer),
    sa.column('flag', sa.Integer),
    sa.column('transformation', sa.String),
    sa.column('created_timestamp', sa.DateTime),
    sa.column('updated_timestamp', sa.DateTime),
)

# TODO: Fill in actual data for each mascot avatar
avatar_configurations = {
    1: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    2: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    3: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    4: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    5: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    6: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    7: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    8: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    9: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    10: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    11: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    12: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    13: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    14: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    15: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    16: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    17: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    18: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    19: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    20: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    21: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    22: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    23: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    24: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
    25: {'color': 1, 'head': 0, 'face': 0, 'neck': 0, 'body': 0, 'hand': 0, 'feet': 0, 'photo': 0, 'flag': 0},
}


def add_user(entry: Tuple[Any]) -> None:
    print(f"[{users_table.name}] Inserting row for '{entry[2]}'...")

    # Insert a the avatar and get its ID
    avatar_query = (
        sa.insert(avatars_table)
          .values(**avatar_configurations[entry[0]])
          .returning(avatars_table.c.id)
    )
    avatar_id = op.get_bind().execute(avatar_query).scalar()

    # Create a query to fetch the corresponding mascot ID
    mascot_query = (
        sa.select(mascots_table.c.id)
          .where(mascots_table.c.name == entry[2])
    )

    # Create the user
    user_query = sa.insert(users_table).values(
        id=entry[0],
        username=entry[1],
        nickname=entry[2],
        password=entry[3],
        email=entry[4],
        scopes=entry[5],
        lang=0,
        mascot_id=mascot_query,
        avatar_id=avatar_id
    )
    op.execute(user_query)


def remove_user_entries(user_ids: List[int]) -> None:
    print(f"[{users_table.name}] Deleting {len(user_ids)} rows...")

    for entry in user_ids:
        # Select user's avatar id before deleting
        avatar_query = sa.select(users_table.c.avatar_id).where(users_table.c.id == entry)
        avatar_id = op.get_bind().execute(avatar_query).scalar()

        op.execute(users_table.delete().where(users_table.c.id == entry))
        op.execute(avatars_table.delete().where(avatars_table.c.id == avatar_id))


def upgrade() -> None:
    for entry in users_data:
        add_user(entry)


def downgrade() -> None:
    remove_user_entries([row[0] for row in users_data])
