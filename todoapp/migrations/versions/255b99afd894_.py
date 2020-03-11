"""empty message

Revision ID: 255b99afd894
Revises: b13485fcefef
Create Date: 2020-03-10 19:04:38.439077

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255b99afd894'
down_revision = 'b13485fcefef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('todos', 'list_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###