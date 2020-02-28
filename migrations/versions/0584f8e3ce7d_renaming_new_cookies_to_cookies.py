"""Renaming new_cookies to cookies

Revision ID: 0584f8e3ce7d
Revises: 2ab2e0def1db
Create Date: 2020-02-28 14:39:36.971635

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0584f8e3ce7d'
down_revision = '2ab2e0def1db'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('new_cookies', 'cookies')


def downgrade():
    op.rename_table('cookies', 'new_cookies')
