"""empty message

Revision ID: 9934a1385681
Revises: 
Create Date: 2018-06-06 11:42:48.132036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9934a1385681'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('letter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('parentId', sa.Integer(), nullable=True),
    sa.Column('regionName', sa.String(length=50), nullable=True),
    sa.Column('cityCode', sa.Integer(), nullable=True),
    sa.Column('pinYin', sa.String(length=100), nullable=True),
    sa.Column('letter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['letter_id'], ['letter.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('city')
    op.drop_table('letter')
    # ### end Alembic commands ###