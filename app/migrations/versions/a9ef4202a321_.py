"""empty message

Revision ID: a9ef4202a321
Revises: b10cb8153816
Create Date: 2024-03-19 19:56:26.038715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9ef4202a321'
down_revision: Union[str, None] = 'b10cb8153816'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
