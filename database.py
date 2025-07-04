"""
Conexão com banco de dados PostgreSQL.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do banco
# Se não conseguir carregar do .env, usar a URL codificada diretamente
try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL or 'Segura123!' in DATABASE_URL:
        # Usar URL com senha codificada se houver problema
        DATABASE_URL = 'postgresql://thetrace_user:MinhaSenh%40Segura123%21@localhost:5432/thetrace_db'
except Exception:
    DATABASE_URL = 'postgresql://thetrace_user:MinhaSenh%40Segura123%21@localhost:5432/thetrace_db'

# Engine e session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Retorna uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Cria todas as tabelas no banco de dados."""
    Base.metadata.create_all(bind=engine)

def get_stats():
    """Retorna estatísticas básicas das tabelas."""
    with SessionLocal() as db:
        from sqlalchemy import text
        
        # Aeródromos privados
        try:
            privados_count = db.execute(text("SELECT COUNT(*) FROM aerodromos_privados")).scalar()
            privados_coords = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_privados 
                WHERE lat_geo_point IS NOT NULL AND lon_geo_point IS NOT NULL
            """)).scalar()
            privados_oaci = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_privados 
                WHERE codigo_oaci IS NOT NULL AND codigo_oaci != ''
            """)).scalar()
        except:
            privados_count = 0
            privados_coords = 0
            privados_oaci = 0
        
        # Aeródromos públicos
        try:
            publicos_count = db.execute(text("SELECT COUNT(*) FROM aerodromos_publicos")).scalar()
            publicos_coords = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_publicos 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)).scalar()
            publicos_oaci = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_publicos 
                WHERE codigo_oaci IS NOT NULL AND codigo_oaci != ''
            """)).scalar()
        except:
            publicos_count = 0
            publicos_coords = 0
            publicos_oaci = 0
        
        return {
            'aerodromos_privados': {
                'total': privados_count,
                'com_coordenadas': privados_coords,
                'sem_coordenadas': privados_count - privados_coords,
                'com_codigo_oaci': privados_oaci
            },
            'aerodromos_publicos': {
                'total': publicos_count,
                'com_coordenadas': publicos_coords,
                'sem_coordenadas': publicos_count - publicos_coords,
                'com_codigo_oaci': publicos_oaci
            }
        }
