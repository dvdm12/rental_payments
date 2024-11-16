"""i've modified constraint on payments table

Revision ID: ae6e51ec03c7
Revises: 8261c954d135
Create Date: 2024-10-09 03:04:45.874608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae6e51ec03c7'
down_revision = '8261c954d135'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Eliminar la clave primaria actual
    op.drop_constraint('payments_pkey', 'payments', type_='primary')

    # Añadir property_code como nueva clave primaria y mantener tenant_id_number como clave foránea
    op.create_primary_key('pk_payments', 'payments', ['property_code'])

    # Elimina la clave foránea si existe
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint('fk_tenant', type_='foreignkey')

    # Añadir tenant_id_number como clave foránea hacia tenants
    op.create_foreign_key('fk_tenant', 'payments', 'tenants', ['tenant_id_number'], ['tenant_id_number'])


def downgrade() -> None:
    # Eliminar la clave foránea de tenant_id_number
    op.drop_constraint('fk_tenant', 'payments', type_='foreignkey')

    # Eliminar la clave primaria en property_code
    op.drop_constraint('pk_payments', 'payments', type_='primary')

    # Restaurar tenant_id_number como clave primaria
    op.create_primary_key('payments_pkey', 'payments', ['tenant_id_number'])
