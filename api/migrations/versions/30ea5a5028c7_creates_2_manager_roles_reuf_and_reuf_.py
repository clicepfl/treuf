"""creates 2 manager roles: reuf and reuf_admin

Revision ID: 30ea5a5028c7
Revises: 75535bf06e66
Create Date: 2022-06-13 18:01:40.892655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30ea5a5028c7'
down_revision = '75535bf06e66'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_reuf_admin', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('is_reuf', sa.Boolean(), nullable=True))
    op.drop_column('user', 'is_admin')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_admin', sa.BOOLEAN(), nullable=True))
    op.drop_column('user', 'is_reuf')
    op.drop_column('user', 'is_reuf_admin')
    # ### end Alembic commands ###