"""story database

Revision ID: adbf3234da03
Revises: 794b179f951b
Create Date: 2017-10-11 20:45:00.830216

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adbf3234da03'
down_revision = '794b179f951b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('story_string', sa.String, nullable=False),
        sa.Column('author', sa.String, nullable=False),
        sa.Column('story_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )


def downgrade():
    op.drop_table('stories')
