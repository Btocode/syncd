"""initial_migration

Revision ID: 18c20e550da0
Revises:
Create Date: 2025-04-29 09:16:23.951054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Import your models
from app.db.models import User, Device


# revision identifiers, used by Alembic.
revision: str = '18c20e550da0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table('users',
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=True),
        sa.Column('display_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('user_id'),
        sa.UniqueConstraint('email')
    )

    # Create devices table
    op.create_table('devices',
        sa.Column('device_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('device_name', sa.String(), nullable=False),
        sa.Column('os_name', sa.String(), nullable=False),
        sa.Column('os_version', sa.String(), nullable=False),
        sa.Column('browser_name', sa.String(), nullable=True),
        sa.Column('browser_version', sa.String(), nullable=True),
        sa.Column('last_login', sa.DateTime(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
        sa.PrimaryKeyConstraint('device_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop tables in reverse order to avoid foreign key constraints
    op.drop_table('devices')
    op.drop_table('users')
