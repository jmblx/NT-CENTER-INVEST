"""empty message

Revision ID: 31cb5ae0d33a
Revises: fa0b310cebb3
Create Date: 2024-04-13 14:01:22.895711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '31cb5ae0d33a'
down_revision: Union[str, None] = 'fa0b310cebb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('tg_id', sa.String(length=20), nullable=True))
    op.add_column('user', sa.Column('tg_settings', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    op.create_unique_constraint(None, 'user', ['tg_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'tg_settings')
    op.drop_column('user', 'tg_id')
    # ### end Alembic commands ###
