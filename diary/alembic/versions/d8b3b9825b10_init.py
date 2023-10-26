"""init

Revision ID: d8b3b9825b10
Revises: 
Create Date: 2023-10-26 21:36:40.192730

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'd8b3b9825b10'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_account',
    sa.Column('telegram_id', sa.Integer(), nullable=False),
    sa.Column('phpsessid', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('telegram_id'),
    sa.UniqueConstraint('telegram_id')
    )
    op.create_table('parcipiants_id',
    sa.Column('parcipiant_id', sa.String(), nullable=False),
    sa.Column('is_current', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.telegram_id'], ),
    sa.PrimaryKeyConstraint('parcipiant_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parcipiants_id')
    op.drop_table('user_account')
    # ### end Alembic commands ###