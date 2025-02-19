"""added latitude,longitude

Revision ID: d26d99ecfe94
Revises: 64325f20cfe5
Create Date: 2025-02-19 11:29:45.455208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd26d99ecfe94'
down_revision: Union[str, None] = '64325f20cfe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('branches', sa.Column('latitude', sa.Numeric(precision=9, scale=6), nullable=True))
    op.add_column('branches', sa.Column('longitude', sa.Numeric(precision=9, scale=6), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('branches', 'longitude')
    op.drop_column('branches', 'latitude')
    # ### end Alembic commands ###
