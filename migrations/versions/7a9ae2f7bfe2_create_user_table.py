"""create User table

Revision ID: 7a9ae2f7bfe2
Revises: 
Create Date: 2022-10-30 07:33:16.300202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a9ae2f7bfe2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
