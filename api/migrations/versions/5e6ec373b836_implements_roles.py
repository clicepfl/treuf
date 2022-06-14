"""implements roles

Revision ID: 5e6ec373b836
Revises: 30ea5a5028c7
Create Date: 2022-06-14 15:07:02.728236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e6ec373b836'
down_revision = '30ea5a5028c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('roles', sa.PickleType(), nullable=True))
    op.drop_column('user', 'is_reuf_admin')
    op.drop_column('user', 'is_reuf')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_reuf', sa.BOOLEAN(), nullable=True))
    op.add_column('user', sa.Column('is_reuf_admin', sa.BOOLEAN(), nullable=True))
    op.drop_column('user', 'roles')
    # ### end Alembic commands ###
