"""remove is_delete column

Revision ID: 464d6d4b717a
Revises: 08317091e4a8
Create Date: 2020-11-15 19:33:59.211386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '464d6d4b717a'
down_revision = '08317091e4a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_category_title', table_name='category')
    op.create_index(op.f('ix_category_title'), 'category', ['title'], unique=True)
    op.drop_column('category', 'is_deleted')
    op.drop_column('item', 'is_deleted')
    op.drop_index('ix_payment_title', table_name='payment')
    op.create_index(op.f('ix_payment_title'), 'payment', ['title'], unique=True)
    op.drop_column('payment', 'is_deleted')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_payment_title'), table_name='payment')
    op.create_index('ix_payment_title', 'payment', ['title'], unique=False)
    op.add_column('item', sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('category', sa.Column('is_deleted', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_category_title'), table_name='category')
    op.create_index('ix_category_title', 'category', ['title'], unique=False)
    # ### end Alembic commands ###
