"""add notification status

Revision ID: f1322c6c5a17
Revises: 62d2f4b50940
Create Date: 2023-11-20 19:31:20.289711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1322c6c5a17'
down_revision: Union[str, None] = '62d2f4b50940'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_account', sa.Column('notification_status', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_account', 'notification_status')
    # ### end Alembic commands ###
