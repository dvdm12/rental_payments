"""create tables again

Revision ID: 8261c954d135
Revises: 6e9fcbc2f174
Create Date: 2024-10-08 22:17:16.525100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8261c954d135'
down_revision = '6e9fcbc2f174'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('tenant_id_number', sa.String(), nullable=False),
    sa.Column('property_code', sa.String(), nullable=True),
    sa.Column('paid_amount', sa.Numeric(), nullable=True),
    sa.Column('payment_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('tenant_id_number')
    )
    op.create_table('tenants',
    sa.Column('tenant_id_number', sa.String(), nullable=False),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('tenant_id_number'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tenants')
    op.drop_table('payments')
    # ### end Alembic commands ###
