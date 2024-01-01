"""Added data to user table

Revision ID: 64b03e0ab989
Revises: 11ae9ee31d92
Create Date: 2023-09-05 22:04:02.445249

"""
from typing import Sequence, Union

from login import User
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '64b03e0ab989'
down_revision: Union[str, None] = '11ae9ee31d92'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(User.__table__,
                   [
                       {
                           'id': 1,
                           'password': '65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5',
                       },
                   ])


def downgrade() -> None:
    pass
