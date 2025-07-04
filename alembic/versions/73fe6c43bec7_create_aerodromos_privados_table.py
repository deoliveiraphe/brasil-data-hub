"""Create aerodromos_privados table

Revision ID: 73fe6c43bec7
Revises: 
Create Date: 2025-07-01 11:02:11.537188

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '73fe6c43bec7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Criar tabela aerodromos_privados
    op.create_table(
        'aerodromos_privados',
        
        # Chave primária
        sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        
        # Dados principais do aeródromo
        sa.Column('codigo_oaci', sa.String(4), nullable=True, comment='Código OACI do aeródromo (4 caracteres)'),
        sa.Column('ciad', sa.String(20), nullable=True, comment='Código de Identificação do Aeródromo'),
        sa.Column('nome', sa.String(255), nullable=False, comment='Nome do aeródromo'),
        sa.Column('municipio', sa.String(100), nullable=True, comment='Município onde está localizado o aeródromo'),
        sa.Column('uf', sa.String(2), nullable=True, comment='Unidade Federativa do aeródromo'),
        sa.Column('municipio_servido', sa.String(100), nullable=True, comment='Município servido pelo aeródromo'),
        sa.Column('uf_servido', sa.String(2), nullable=True, comment='UF do município servido pelo aeródromo'),
        
        # Coordenadas geográficas
        sa.Column('lat_geo_point', sa.Float(precision=8), nullable=True, comment='Latitude em formato decimal'),
        sa.Column('lon_geo_point', sa.Float(precision=8), nullable=True, comment='Longitude em formato decimal'),
        
        # Metadados de controle
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment='Data/hora de criação do registro'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False, comment='Data/hora da última atualização'),
        sa.Column('scraped_at', sa.DateTime(timezone=True), nullable=True, comment='Data/hora do scraping dos dados'),
        sa.Column('source_url', sa.Text, nullable=True, comment='URL da fonte dos dados'),
        
        # Constraints de validação
        sa.CheckConstraint('uf IS NULL OR length(uf) = 2', name='ck_aerodromos_privados_uf_length'),
        sa.CheckConstraint('uf_servido IS NULL OR length(uf_servido) = 2', name='ck_aerodromos_privados_uf_servido_length'),
        sa.CheckConstraint('codigo_oaci IS NULL OR length(codigo_oaci) <= 4', name='ck_aerodromos_privados_codigo_oaci_length'),
        sa.CheckConstraint('lat_geo_point IS NULL OR (lat_geo_point >= -90 AND lat_geo_point <= 90)', name='ck_aerodromos_privados_latitude_range'),
        sa.CheckConstraint('lon_geo_point IS NULL OR (lon_geo_point >= -180 AND lon_geo_point <= 180)', name='ck_aerodromos_privados_longitude_range'),
        
        comment='Tabela de aeródromos privados coletados da ANAC'
    )
    
    # Criar índices para performance
    op.create_index('ix_aerodromos_privados_codigo_oaci', 'aerodromos_privados', ['codigo_oaci'])
    op.create_index('ix_aerodromos_privados_ciad', 'aerodromos_privados', ['ciad'])
    op.create_index('ix_aerodromos_privados_uf', 'aerodromos_privados', ['uf'])
    op.create_index('ix_aerodromos_privados_municipio', 'aerodromos_privados', ['municipio'])
    op.create_index('ix_aerodromos_privados_nome', 'aerodromos_privados', ['nome'])
    op.create_index('ix_aerodromos_privados_coords', 'aerodromos_privados', ['lat_geo_point', 'lon_geo_point'])
    op.create_index('ix_aerodromos_privados_created_at', 'aerodromos_privados', ['created_at'])
    
    # Índice único composto para evitar duplicatas
    op.create_index(
        'ix_aerodromos_privados_unique_identifier', 
        'aerodromos_privados', 
        ['codigo_oaci', 'ciad', 'nome'],
        unique=True,
        postgresql_where=sa.text('codigo_oaci IS NOT NULL OR ciad IS NOT NULL')
    )


def downgrade() -> None:
    # Remover tabela aerodromos_privados
    op.drop_table('aerodromos_privados')
