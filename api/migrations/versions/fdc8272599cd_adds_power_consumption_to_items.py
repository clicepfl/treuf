"""adds power consumption to items

Revision ID: fdc8272599cd
Revises: 5e6ec373b836
Create Date: 2022-06-14 18:11:13.770139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdc8272599cd'
down_revision = '5e6ec373b836'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('power', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'power')
    # ### end Alembic commands ###
