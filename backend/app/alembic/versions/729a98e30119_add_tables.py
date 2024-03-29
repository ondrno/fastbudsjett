"""add tables

Revision ID: 729a98e30119
Revises: d4867f3a4c0a
Create Date: 2020-12-09 23:12:14.178891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '729a98e30119'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('itemtype',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_itemtype_id'), 'itemtype', ['id'], unique=False)
    op.create_index(op.f('ix_itemtype_name'), 'itemtype', ['name'], unique=True)
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_payment_id'), 'payment', ['id'], unique=False)
    op.create_index(op.f('ix_payment_name'), 'payment', ['name'], unique=True)
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('itemtype_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['itemtype_id'], ['itemtype.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.add_column('item', sa.Column('amount', sa.Float(), nullable=False))
    op.add_column('item', sa.Column('category_id', sa.Integer(), nullable=False))
    op.add_column('item', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('item', sa.Column('date', sa.Date(), nullable=False))
    op.add_column('item', sa.Column('itemtype_id', sa.Integer(), nullable=False))
    op.add_column('item', sa.Column('modified_at', sa.DateTime(), nullable=True))
    op.add_column('item', sa.Column('payment_id', sa.Integer(), nullable=False))
    op.add_column('item', sa.Column('removed_at', sa.DateTime(), nullable=True))
    op.alter_column('item', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('item', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_index('ix_item_title', table_name='item')
    op.create_foreign_key(None, 'item', 'payment', ['payment_id'], ['id'])
    op.create_foreign_key(None, 'item', 'itemtype', ['itemtype_id'], ['id'])
    op.create_foreign_key(None, 'item', 'category', ['category_id'], ['id'])
    op.drop_column('item', 'title')
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('item', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.drop_constraint(None, 'item', type_='foreignkey')
    op.create_index('ix_item_title', 'item', ['title'], unique=False)
    op.alter_column('item', 'owner_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('item', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('item', 'removed_at')
    op.drop_column('item', 'payment_id')
    op.drop_column('item', 'modified_at')
    op.drop_column('item', 'itemtype_id')
    op.drop_column('item', 'date')
    op.drop_column('item', 'created_at')
    op.drop_column('item', 'category_id')
    op.drop_column('item', 'amount')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_table('category')
    op.drop_index(op.f('ix_payment_name'), table_name='payment')
    op.drop_index(op.f('ix_payment_id'), table_name='payment')
    op.drop_table('payment')
    op.drop_index(op.f('ix_itemtype_name'), table_name='itemtype')
    op.drop_index(op.f('ix_itemtype_id'), table_name='itemtype')
    op.drop_table('itemtype')
    # ### end Alembic commands ###
