"""
Scraper para municípios defrontantes com o mar do IBGE.
Baixa e processa dados de arquivo Excel.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import io

import requests
import pandas as pd
from sqlalchemy import text

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from database import SessionLocal, create_tables
from models import MunicipioMaritimo
from utils import cleanup_data_files

class MunicipiosMaritimosIBGEScraper:
    """Scraper específico para municípios defrontantes com o mar do IBGE."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, */*'
        })
        
        # URL do arquivo Excel do IBGE
        self.url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/municipios_defrontantes_com_o_mar/2024/Municipios_Defrontantes_com_o_Mar_2024.xls'
        
        # Criar pastas se não existirem
        Path('data').mkdir(exist_ok=True)
        Path('data/raw').mkdir(exist_ok=True)
        Path('data/processed').mkdir(exist_ok=True)
    
    def fetch_data(self) -> pd.DataFrame:
        """Baixa e carrega o arquivo Excel do IBGE."""
        print("🔍 Buscando dados de municípios marítimos do IBGE...")
        
        try:
            response = self.session.get(self.url, timeout=60)
            response.raise_for_status()
            
            # Salvar dados brutos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_file = f'data/raw/municipios_maritimos_raw_{timestamp}.xls'
            
            with open(raw_file, 'wb') as f:
                f.write(response.content)
            
            # Ler Excel com pandas - arquivo .xls antigo
            # Primeiro, tentar determinar o tipo real do arquivo
            content_type = response.headers.get('content-type', '').lower()
            print(f"🔍 Content-Type: {content_type}")
            
            # Salvar temporariamente para análise
            temp_bytes = response.content
            print(f"🔍 Primeiros bytes: {temp_bytes[:10]}")
            
            # Tentar ler como Excel antigo (.xls)
            try:
                df = pd.read_excel(io.BytesIO(temp_bytes), engine='xlrd')
                print("✅ Lido com xlrd (Excel antigo)")
            except Exception as e1:
                print(f"⚠️ Erro com xlrd: {e1}")
                
                # Tentar openpyxl (Excel moderno)
                try:
                    df = pd.read_excel(io.BytesIO(temp_bytes), engine='openpyxl')
                    print("✅ Lido com openpyxl (Excel moderno)")
                except Exception as e2:
                    print(f"⚠️ Erro com openpyxl: {e2}")
                    
                    # Tentar sem especificar engine
                    try:
                        df = pd.read_excel(io.BytesIO(temp_bytes))
                        print("✅ Lido com engine automático")
                    except Exception as e3:
                        print(f"⚠️ Erro com engine automático: {e3}")
                        
                        # Se tudo falhar, talvez seja um CSV disfarçado
                        try:
                            # Tentar como CSV
                            content_str = temp_bytes.decode('utf-8', errors='ignore')
                            if '\t' in content_str[:1000]:  # TSV
                                df = pd.read_csv(io.StringIO(content_str), sep='\t')
                                print("✅ Lido como TSV")
                            elif ',' in content_str[:1000]:  # CSV
                                df = pd.read_csv(io.StringIO(content_str))
                                print("✅ Lido como CSV")
                            else:
                                raise Exception("Formato de arquivo não reconhecido")
                        except Exception as e4:
                            raise Exception(f"Falha ao ler arquivo: xlrd={e1}, openpyxl={e2}, auto={e3}, csv={e4}")
            
            print(f"✅ {len(df)} municípios marítimos encontrados")
            print(f"📁 Arquivo salvo em: {raw_file}")
            
            return df
            
        except requests.RequestException as e:
            print(f"❌ Erro ao buscar dados: {e}")
            raise
        except Exception as e:
            print(f"❌ Erro ao processar Excel: {e}")
            raise
    
    def process_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Processa e limpa os dados do DataFrame."""
        print("🔧 Processando dados...")
        
        processed_municipios = []
        
        # Mapear nomes das colunas esperadas
        column_mapping = {
            'CD_MUN': 'cd_mun',
            'NM_MUN': 'nm_mun', 
            'CD_RGI': 'cd_rgi',
            'NM_RGI': 'nm_rgi',
            'CD_RGINT': 'cd_rgint',
            'NM_RGINT': 'nm_rgint',
            'CD_UF': 'cd_uf',
            'NM_UF': 'nm_uf',
            'SIGLA_UF': 'sigla_uf',
            'CD_REGIA': 'cd_regia',
            'NM_REGIA': 'nm_regia',
            'SIGLA_RG': 'sigla_rg',
            'AREA_KM2': 'area_km2'
        }
        
        # Verificar se as colunas esperadas existem
        print(f"🔍 Colunas encontradas: {list(df.columns)}")
        
        # Ajustar nomes das colunas se necessário
        df_clean = df.copy()
        
        # Renomear colunas se necessário
        for old_col, new_col in column_mapping.items():
            if old_col in df_clean.columns:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        for idx, row in df_clean.iterrows():
            try:
                # Extrair e limpar dados
                municipio = {
                    'cd_mun': self._clean_string(row.get('cd_mun')),
                    'nm_mun': self._clean_string(row.get('nm_mun')),
                    'cd_rgi': self._clean_string(row.get('cd_rgi')),
                    'nm_rgi': self._clean_string(row.get('nm_rgi')),
                    'cd_rgint': self._clean_string(row.get('cd_rgint')),
                    'nm_rgint': self._clean_string(row.get('nm_rgint')),
                    'cd_uf': self._clean_string(row.get('cd_uf')),
                    'nm_uf': self._clean_string(row.get('nm_uf')),
                    'sigla_uf': self._clean_string(row.get('sigla_uf')),
                    'cd_regia': self._clean_string(row.get('cd_regia')),
                    'nm_regia': self._clean_string(row.get('nm_regia')),
                    'sigla_rg': self._clean_string(row.get('sigla_rg')),
                    'area_km2': self._parse_float(row.get('area_km2')),
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': self.url
                }
                
                # Validar dados obrigatórios
                if not municipio['cd_mun'] or not municipio['nm_mun']:
                    print(f"⚠️ Município sem código ou nome ignorado na linha {idx}: {row.to_dict()}")
                    continue
                
                processed_municipios.append(municipio)
                
            except Exception as e:
                print(f"⚠️ Erro ao processar linha {idx}: {e}")
                continue
        
        # Salvar dados processados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_file = f'data/processed/municipios_maritimos_{timestamp}.json'
        
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(processed_municipios, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(processed_municipios)} municípios processados")
        print(f"📁 Dados salvos em: {processed_file}")
        
        return processed_municipios
    
    def _clean_string(self, value: Any) -> Optional[str]:
        """Limpa e valida strings."""
        if value is None or pd.isna(value):
            return None
        
        cleaned = str(value).strip()
        return cleaned if cleaned and cleaned.upper() not in ['NULL', 'NONE', 'N/A', 'NAN'] else None
    
    def _parse_float(self, value: Any) -> Optional[float]:
        """Converte valor para float."""
        if value is None or pd.isna(value):
            return None
        
        try:
            if isinstance(value, (int, float)):
                return float(value)
            
            # Se for string, tentar converter
            value_str = str(value).replace(',', '.').strip()
            if not value_str or value_str.upper() in ['NULL', 'NONE', 'N/A', 'NAN']:
                return None
                
            return float(value_str)
            
        except (ValueError, TypeError):
            return None
    
    def save_to_database(self, municipios: List[Dict[str, Any]]) -> int:
        """Salva os dados no banco PostgreSQL."""
        print("💾 Salvando no banco de dados...")
        
        # Criar tabelas se não existirem
        create_tables()
        
        saved_count = 0
        
        with SessionLocal() as db:
            try:
                # Limpar tabela existente
                db.execute(text("TRUNCATE TABLE municipios_maritimos RESTART IDENTITY CASCADE"))
                
                # Inserir dados
                for data in municipios:
                    municipio = MunicipioMaritimo(
                        cd_mun=data.get('cd_mun'),
                        nm_mun=data['nm_mun'],
                        cd_rgi=data.get('cd_rgi'),
                        nm_rgi=data.get('nm_rgi'),
                        cd_rgint=data.get('cd_rgint'),
                        nm_rgint=data.get('nm_rgint'),
                        cd_uf=data.get('cd_uf'),
                        nm_uf=data.get('nm_uf'),
                        sigla_uf=data.get('sigla_uf'),
                        cd_regia=data.get('cd_regia'),
                        nm_regia=data.get('nm_regia'),
                        sigla_rg=data.get('sigla_rg'),
                        area_km2=data.get('area_km2'),
                        scraped_at=datetime.fromisoformat(data['scraped_at']),
                        source_url=data['source_url']
                    )
                    db.add(municipio)
                    saved_count += 1
                
                db.commit()
                print(f"✅ {saved_count} municípios salvos no banco")
                
            except Exception as e:
                db.rollback()
                print(f"❌ Erro ao salvar no banco: {e}")
                raise
        
        return saved_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da tabela."""
        with SessionLocal() as db:
            # Contadores básicos
            total = db.execute(text("SELECT COUNT(*) FROM municipios_maritimos")).scalar()
            
            com_area = db.execute(text("""
                SELECT COUNT(*) FROM municipios_maritimos 
                WHERE area_km2 IS NOT NULL
            """)).scalar()
            
            # Top UFs
            top_ufs = db.execute(text("""
                SELECT sigla_uf, COUNT(*) as count 
                FROM municipios_maritimos 
                WHERE sigla_uf IS NOT NULL 
                GROUP BY sigla_uf 
                ORDER BY count DESC 
                LIMIT 5
            """)).fetchall()
            
            # Top regiões
            top_regioes = db.execute(text("""
                SELECT nm_regia, COUNT(*) as count 
                FROM municipios_maritimos 
                WHERE nm_regia IS NOT NULL 
                GROUP BY nm_regia 
                ORDER BY count DESC
            """)).fetchall()
            
            # Área total
            area_total = db.execute(text("""
                SELECT SUM(area_km2) FROM municipios_maritimos 
                WHERE area_km2 IS NOT NULL
            """)).scalar()
            
            return {
                'total_municipios': total,
                'com_area': com_area,
                'sem_area': total - com_area,
                'area_total_km2': float(area_total) if area_total else 0,
                'top_ufs': [{'uf': row[0], 'count': row[1]} for row in top_ufs],
                'top_regioes': [{'regiao': row[0], 'count': row[1]} for row in top_regioes]
            }
    
    def run(self) -> Dict[str, Any]:
        """Executa o scraping completo."""
        print("🚀 Iniciando scraping de municípios marítimos do IBGE...")
        start_time = time.time()
        
        try:
            # 1. Buscar dados
            df = self.fetch_data()
            
            # 2. Processar dados
            processed_data = self.process_data(df)
            
            # 3. Salvar no banco
            saved_count = self.save_to_database(processed_data)
            
            # 4. Estatísticas
            stats = self.get_stats()
            
            # 5. Limpeza de arquivos antigos
            cleanup_data_files('municipios_maritimos')
            
            elapsed_time = time.time() - start_time
            
            result = {
                'success': True,
                'raw_count': len(df),
                'processed_count': len(processed_data),
                'saved_count': saved_count,
                'elapsed_time': elapsed_time,
                'stats': stats
            }
            
            print(f"\n📊 Resumo do scraping:")
            print(f"   ⏱️ Tempo: {elapsed_time:.2f}s")
            print(f"   📥 Dados brutos: {len(df)}")
            print(f"   🔧 Processados: {len(processed_data)}")
            print(f"   💾 Salvos no banco: {saved_count}")
            print(f"   📍 Com área: {stats['com_area']}")
            print(f"   📐 Área total: {stats['area_total_km2']:.2f} km²")
            
            if stats['top_ufs']:
                print(f"\n🏆 Top UFs:")
                for uf_data in stats['top_ufs']:
                    print(f"   {uf_data['uf']}: {uf_data['count']} municípios")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro durante o scraping: {e}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }

if __name__ == '__main__':
    scraper = MunicipiosMaritimosIBGEScraper()
    result = scraper.run()
    
    if result['success']:
        print("\n🎉 Scraping concluído com sucesso!")
    else:
        print(f"\n💥 Scraping falhou: {result['error']}")
