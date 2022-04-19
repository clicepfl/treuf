"""adds return date

Revision ID: b771fec69a49
Revises: d2427d186a63
Create Date: 2022-04-19 21:54:32.298548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b771fec69a49'
down_revision = 'd2427d186a63'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowing', sa.Column('return_date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('borrowing', 'return_date')
    # ### end Alembic commands ###
