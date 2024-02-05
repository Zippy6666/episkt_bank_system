"""empty message

Revision ID: 31fdf7093e66
Revises: 8352e8924a34
Create Date: 2024-02-01 13:56:17.487639

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '31fdf7093e66'
down_revision = '8352e8924a34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('belopp', sa.Float(), nullable=False),
    sa.Column('typ', sa.String(length=6), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
