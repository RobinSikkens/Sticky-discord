"""create tellen table

Revision ID: 2cf458912ec4
Revises: 
Create Date: 2017-10-09 12:16:00.225642

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2cf458912ec4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tellen',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('count', sa.Integer, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )

def downgrade():
    op.drop_table('tellen')
