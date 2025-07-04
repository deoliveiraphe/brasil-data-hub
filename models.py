"""
Modelos de dados para aeródromos da ANAC.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, Float, DateTime, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class AerodromoPrivado(Base):
    """Modelo para aeródromos privados da ANAC."""
    
    __tablename__ = "aerodromos_privados"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificadores
    codigo_oaci = Column(String(4), nullable=True, index=True, comment="Código OACI do aeródromo")
    ciad = Column(Text, nullable=True, index=True, comment="Código de Identificação do Aeródromo")
    
    # Dados básicos
    nome = Column(String(255), nullable=False, index=True, comment="Nome do aeródromo")
    municipio = Column(String(100), nullable=True, index=True, comment="Município")
    uf = Column(String(50), nullable=True, index=True, comment="Unidade Federativa")
    
    # Coordenadas
    lat_geo_point = Column(Float, nullable=True, comment="Latitude")
    lon_geo_point = Column(Float, nullable=True, comment="Longitude")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<AerodromoPrivado(nome='{self.nome}', municipio='{self.municipio}', uf='{self.uf}')>"

class AerodromoPublico(Base):
    """Modelo para aeródromos públicos da ANAC."""
    
    __tablename__ = "aerodromos_publicos"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificadores
    codigo_oaci = Column(String(4), nullable=True, index=True, comment="Código OACI do aeródromo")
    ciad = Column(Text, nullable=True, index=True, comment="Código de Identificação do Aeródromo")
    
    # Dados básicos
    nome = Column(String(255), nullable=False, index=True, comment="Nome do aeródromo")
    municipio = Column(String(100), nullable=True, index=True, comment="Município")
    uf = Column(String(50), nullable=True, index=True, comment="Unidade Federativa")
    
    # Coordenadas (nomenclatura diferente dos privados)
    latitude = Column(Float, nullable=True, comment="Latitude")
    longitude = Column(Float, nullable=True, comment="Longitude")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<AerodromoPublico(nome='{self.nome}', municipio='{self.municipio}', uf='{self.uf}')>"

class MunicipioMaritimo(Base):
    """Modelo para municípios defrontantes com o mar do IBGE."""
    
    __tablename__ = "municipios_maritimos"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dados do município
    cd_mun = Column(String(7), nullable=False, index=True, comment="Código do município")
    nm_mun = Column(Text, nullable=False, index=True, comment="Nome do município")
    
    # Dados da região geográfica imediata
    cd_rgi = Column(Text, nullable=True, comment="Código da região geográfica imediata")
    nm_rgi = Column(Text, nullable=True, comment="Nome da região geográfica imediata")
    
    # Dados da região geográfica intermediária
    cd_rgint = Column(Text, nullable=True, comment="Código da região geográfica intermediária")
    nm_rgint = Column(Text, nullable=True, comment="Nome da região geográfica intermediária")
    
    # Dados da UF
    cd_uf = Column(String(2), nullable=False, index=True, comment="Código da UF")
    nm_uf = Column(Text, nullable=False, index=True, comment="Nome da UF")
    sigla_uf = Column(String(2), nullable=False, index=True, comment="Sigla da UF")
    
    # Dados da região
    cd_regia = Column(String(1), nullable=False, comment="Código da região")
    nm_regia = Column(Text, nullable=False, comment="Nome da região")
    sigla_rg = Column(String(2), nullable=False, comment="Sigla da região")
    
    # Área do município
    area_km2 = Column(Float, nullable=True, comment="Área do município em km²")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<MunicipioMaritimo(nome='{self.nm_mun}', uf='{self.sigla_uf}', area={self.area_km2})>"

class MunicipioFronteira(Base):
    """Modelo para municípios da faixa de fronteira e cidades gêmeas do IBGE."""
    
    __tablename__ = "municipios_fronteira"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dados do município
    cd_mun = Column(String(7), nullable=False, index=True, comment="Código do município")
    nm_mun = Column(Text, nullable=False, index=True, comment="Nome do município")
    
    # Dados da região geográfica imediata
    cd_rgi = Column(Text, nullable=True, comment="Código da região geográfica imediata")
    nm_rgi = Column(Text, nullable=True, comment="Nome da região geográfica imediata")
    
    # Dados da região geográfica intermediária
    cd_rgint = Column(Text, nullable=True, comment="Código da região geográfica intermediária")
    nm_rgint = Column(Text, nullable=True, comment="Nome da região geográfica intermediária")
    
    # Dados da UF
    cd_uf = Column(String(2), nullable=False, index=True, comment="Código da UF")
    nm_uf = Column(Text, nullable=False, index=True, comment="Nome da UF")
    sigla_uf = Column(String(2), nullable=False, index=True, comment="Sigla da UF")
    
    # Dados da região
    cd_regiao = Column(String(1), nullable=False, comment="Código da região")
    nm_regiao = Column(Text, nullable=False, comment="Nome da região")
    sigla_rg = Column(String(2), nullable=False, comment="Sigla da região")
    
    # Dados específicos da fronteira
    area_tot = Column(Float, nullable=True, comment="Área total do município em km²")
    toca_lim = Column(Text, nullable=True, comment="Toca limite internacional (SIM/NÃO)")
    area_int = Column(Float, nullable=True, comment="Área na faixa de fronteira em km²")
    porc_int = Column(Float, nullable=True, comment="Percentual na faixa de fronteira")
    faixa_sede = Column(Text, nullable=True, comment="Sede na faixa de fronteira (SIM/NÃO)")
    cid_gemea = Column(Text, nullable=True, comment="É cidade gêmea (SIM/NÃO)")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<MunicipioFronteira(nome='{self.nm_mun}', uf='{self.sigla_uf}', cidade_gemea='{self.cid_gemea}')>"

class MunicipioSuframa(Base):
    """Modelo para municípios da SUFRAMA (Zonas Fiscais Especiais)."""
    
    __tablename__ = "municipios_suframa"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dados do município
    cd_mun = Column(String(7), nullable=False, index=True, comment="Código do município")
    nm_mun = Column(Text, nullable=False, index=True, comment="Nome do município")
    
    # Tipo de zona da SUFRAMA
    tipo_zona = Column(Text, nullable=False, index=True, comment="Tipo da zona (ZONA FRANCA DE MANAUS, ÁREAS DE LIVRE COMÉRCIO)")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<MunicipioSuframa(nome='{self.nm_mun}', tipo='{self.tipo_zona}')>"

class AtracacaoPortuaria(Base):
    """Modelo para dados de atracações portuárias da ANTAQ."""
    
    __tablename__ = "atracacoes_portuarias"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Identificadores
    id_atracacao = Column(String(20), nullable=False, index=True, comment="ID único da atracação")
    cdtup = Column(String(10), nullable=True, index=True, comment="Código TUP")
    id_berco = Column(String(20), nullable=True, comment="ID do berço")
    berco = Column(String(100), nullable=True, comment="Nome/número do berço")
    
    # Dados do porto
    porto_atracacao = Column(String(200), nullable=True, index=True, comment="Nome do porto de atracação")
    coordenadas = Column(String(50), nullable=True, comment="Coordenadas lat,lon")
    latitude = Column(Float, nullable=True, comment="Latitude extraída")
    longitude = Column(Float, nullable=True, comment="Longitude extraída")
    apelido_instalacao = Column(Text, nullable=True, comment="Apelido da instalação portuária")
    complexo_portuario = Column(String(200), nullable=True, comment="Complexo portuário")
    tipo_autoridade = Column(String(100), nullable=True, comment="Tipo da autoridade portuária")
    
    # Datas de operação
    data_atracacao = Column(DateTime(timezone=True), nullable=True, comment="Data de atracação")
    data_chegada = Column(DateTime(timezone=True), nullable=True, comment="Data de chegada")
    data_desatracacao = Column(DateTime(timezone=True), nullable=True, comment="Data de desatracação")
    data_inicio_operacao = Column(DateTime(timezone=True), nullable=True, comment="Data de início da operação")
    data_termino_operacao = Column(DateTime(timezone=True), nullable=True, comment="Data de término da operação")
    
    # Dados temporais
    ano = Column(Integer, nullable=True, index=True, comment="Ano da operação")
    mes = Column(String(10), nullable=True, index=True, comment="Mês da operação")
    
    # Dados da operação
    tipo_operacao = Column(String(100), nullable=True, comment="Tipo de operação")
    tipo_navegacao = Column(String(100), nullable=True, comment="Tipo de navegação da atracação")
    nacionalidade_armador = Column(String(10), nullable=True, comment="Nacionalidade do armador")
    flag_mc_operacao = Column(String(10), nullable=True, comment="Flag MC operação atracação")
    terminal = Column(Text, nullable=True, comment="Terminal")
    
    # Localização
    municipio = Column(String(200), nullable=True, index=True, comment="Município")
    uf = Column(String(100), nullable=True, index=True, comment="Unidade Federativa")
    sguf = Column(String(2), nullable=True, index=True, comment="Sigla da UF")
    regiao_geografica = Column(String(50), nullable=True, comment="Região geográfica")
    regiao_hidrografica = Column(String(100), nullable=True, comment="Região hidrográfica")
    instalacao_em_rio = Column(String(10), nullable=True, comment="Instalação portuária em rio")
    numero_capitania = Column(String(20), nullable=True, comment="Número da capitania")
    numero_imo = Column(String(20), nullable=True, comment="Número do IMO")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<AtracacaoPortuaria(id='{self.id_atracacao}', porto='{self.porto_atracacao}', municipio='{self.municipio}')>"

class RepresentacaoFiscal(Base):
    """Modelo para dados de representações fiscais."""
    
    __tablename__ = "representacoes_fiscais"
    
    # Chave primária
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Dados da representação fiscal
    cpf_cnpj = Column(String(20), nullable=False, index=True, comment="CPF ou CNPJ (pode estar mascarado)")
    nome = Column(String(500), nullable=False, index=True, comment="Nome da pessoa física ou jurídica")
    valor_formatado = Column(String(500), nullable=True, comment="Valor formatado com R$ e separadores")
    
    # Categorização
    tipo_documento = Column(String(10), nullable=True, comment="CPF ou CNPJ baseado no número de dígitos")
    
    # Metadados
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=True, comment="Data do scraping")
    source_url = Column(Text, nullable=True, comment="URL da fonte")
    
    def __repr__(self):
        return f"<RepresentacaoFiscal(cpf_cnpj='{self.cpf_cnpj}', nome='{self.nome}', valor='{self.valor_formatado}')>"
