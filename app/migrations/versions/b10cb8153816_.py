"""empty message

Revision ID: b10cb8153816
Revises: a5f080d40e3b
Create Date: 2024-03-19 19:50:37.481306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b10cb8153816'
down_revision: Union[str, None] = 'a5f080d40e3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
