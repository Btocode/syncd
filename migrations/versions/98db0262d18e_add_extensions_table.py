"""Add extensions table

Revision ID: 98db0262d18e
Revises: 18c20e550da0
Create Date: 2025-04-29 09:37:47.074479

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98db0262d18e'
down_revision: Union[str, None] = '18c20e550da0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # The extensions table already exists, so we don't need to create it
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # We don't want to drop the extensions table in the downgrade
    pass
