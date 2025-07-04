"""remove_municipio_servido_and_uf_servido_columns

Revision ID: 785d665af187
Revises: 73fe6c43bec7
Create Date: 2025-07-01 11:27:40.302870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '785d665af187'
down_revision: Union[str, None] = '73fe6c43bec7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remover colunas municipio_servido e uf_servido da tabela aerodromos_privados."""
    # Remover as colunas desnecessárias
    op.drop_column('aerodromos_privados', 'municipio_servido')
    op.drop_column('aerodromos_privados', 'uf_servido')


def downgrade() -> None:
    """Recriar colunas municipio_servido e uf_servido na tabela aerodromos_privados."""
    # Recriar as colunas caso seja necessário fazer rollback
    op.add_column('aerodromos_privados', 
                  sa.Column('municipio_servido', sa.VARCHAR(length=100), nullable=True,
                           comment='Município servido pelo aeródromo'))
    op.add_column('aerodromos_privados', 
                  sa.Column('uf_servido', sa.VARCHAR(length=2), nullable=True,
                           comment='UF do município servido pelo aeródromo'))
