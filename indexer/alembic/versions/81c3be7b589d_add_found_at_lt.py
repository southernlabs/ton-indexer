"""add_found_at_lt

Revision ID: 81c3be7b589d
Revises: db3b70d9b4da
Create Date: 2024-06-02 13:48:48.554605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81c3be7b589d'
down_revision = 'db3b70d9b4da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('jetton_masters', sa.Column('found_at_lt', sa.NUMERIC(), nullable=True))


def downgrade():
    op.drop_column('jetton_masters', 'found_at_lt')
