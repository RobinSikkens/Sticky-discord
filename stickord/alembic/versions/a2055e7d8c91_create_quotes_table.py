"""create quotes table

Revision ID: a2055e7d8c91
Revises: 794b179f951b
Create Date: 2017-10-15 21:08:21.972941

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2055e7d8c91'
down_revision = '794b179f951b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'quotes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('submitter', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )


def downgrade():
    op.drop_table('quotes')
