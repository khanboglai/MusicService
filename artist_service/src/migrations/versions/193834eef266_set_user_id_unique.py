"""set user id unique

Revision ID: 193834eef266
Revises: 177917e85334
Create Date: 2025-05-19 23:57:13.250258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '193834eef266'
down_revision: Union[str, None] = '177917e85334'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('artists_user_id_key', 'artists', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('artists_user_id_key', 'artists', ['user_id'])
    # ### end Alembic commands ###
