"""change nullable for latitude and longirude

Revision ID: f2af37a36305
Revises: d26d99ecfe94
Create Date: 2025-02-19 11:36:37.919653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2af37a36305'
down_revision: Union[str, None] = 'd26d99ecfe94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branches', 'latitude',
               existing_type=sa.NUMERIC(precision=9, scale=6),
               nullable=False)
    op.alter_column('branches', 'longitude',
               existing_type=sa.NUMERIC(precision=9, scale=6),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('branches', 'longitude',
               existing_type=sa.NUMERIC(precision=9, scale=6),
               nullable=True)
    op.alter_column('branches', 'latitude',
               existing_type=sa.NUMERIC(precision=9, scale=6),
               nullable=True)
    # ### end Alembic commands ###
