"""Added subscriptions tables

Revision ID: 3a828a90bf0e
Revises: 6f4e8dd3ea7e
Create Date: 2021-10-25 20:49:41.403191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a828a90bf0e'
down_revision = '6f4e8dd3ea7e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscribe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscribe', sa.String(), nullable=True),
    sa.Column('limits', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subscribeplan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('subscribe_id', sa.Integer(), nullable=True),
    sa.Column('expiration', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['subscribe_id'], ['subscribe.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_unique_constraint(None, 'user', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_table('subscribeplan')
    op.drop_table('subscribe')
    # ### end Alembic commands ###
