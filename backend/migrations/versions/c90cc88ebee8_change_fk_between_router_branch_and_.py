"""change fk between Router, Branch and Shipment

Revision ID: c90cc88ebee8
Revises: 302559c07f0a
Create Date: 2025-02-18 13:42:35.508554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c90cc88ebee8'
down_revision: Union[str, None] = '302559c07f0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
