"""added SAT/PSAT and ACT models

Revision ID: 9c0465fbd1aa
Revises: ed6b867c7651
Create Date: 2025-06-29 14:00:26.050245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c0465fbd1aa'
down_revision: Union[str, Sequence[str], None] = 'ed6b867c7651'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ACTs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('english_score', sa.Integer(), nullable=False),
    sa.Column('math_score', sa.Integer(), nullable=False),
    sa.Column('reading_score', sa.Integer(), nullable=False),
    sa.Column('science_score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['tests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('PSATs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('english_score', sa.Integer(), nullable=False),
    sa.Column('math_score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['tests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('SATs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('english_score', sa.Integer(), nullable=False),
    sa.Column('math_score', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['tests.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('SATs')
    op.drop_table('PSATs')
    op.drop_table('ACTs')
    # ### end Alembic commands ###
