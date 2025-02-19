"""upgrade shipment to add current location

Revision ID: 184ee3b2acc5
Revises: 03db7649fc90
Create Date: 2025-02-18 11:15:08.865606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '184ee3b2acc5'
down_revision: Union[str, None] = '03db7649fc90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shipments', sa.Column('location', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'shipments', 'branches', ['location'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'shipments', type_='foreignkey')
    op.drop_column('shipments', 'location')
    # ### end Alembic commands ###
