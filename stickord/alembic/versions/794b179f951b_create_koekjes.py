"""create koekjes


Revision ID: 794b179f951b
Revises: 2cf458912ec4
Create Date: 2017-10-11 10:58:59.398956

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '794b179f951b'
down_revision = '2cf458912ec4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
            'koekjes',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('count', sa.Integer, nullable=False),
            sa.Column('author', sa.String, nullable=False),
            sa.Column('created_at', sa.DateTime, default=datetime.utcnow)
    )


def downgrade():
    op.drop_table('koekjes')
