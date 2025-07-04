"""
Scraper para municípios das Zonas Fiscais Especiais da SUFRAMA do IBGE.
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
from models import MunicipioSuframa
from utils import cleanup_data_files

class MunicipiosSuframaIBGEScraper:
    """Scraper específico para municípios das Zonas Fiscais Especiais da SUFRAMA do IBGE."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel, */*'
        })
        
        # URL do arquivo Excel do IBGE
        self.url = 'https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/SUFRAMA/2022/Municipios_SUFRAMA.xlsx'
        
        # Criar pastas se não existirem
        Path('data').mkdir(exist_ok=True)
        Path('data/raw').mkdir(exist_ok=True)
        Path('data/processed').mkdir(exist_ok=True)
    
    def fetch_data(self) -> pd.DataFrame:
        """Baixa e carrega o arquivo Excel do IBGE."""
        print("🔍 Buscando dados de municípios SUFRAMA do IBGE...")
        
        try:
            response = self.session.get(self.url, timeout=60)
            response.raise_for_status()
            
            # Salvar dados brutos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_file = f'data/raw/municipios_suframa_raw_{timestamp}.xlsx'
            
            with open(raw_file, 'wb') as f:
                f.write(response.content)
            
            # Ler Excel com pandas
            try:
                df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')
                print("✅ Lido com openpyxl")
            except Exception as e1:
                print(f"⚠️ Erro com openpyxl: {e1}")
                try:
                    df = pd.read_excel(io.BytesIO(response.content))
                    print("✅ Lido com engine automático")
                except Exception as e2:
                    raise Exception(f"Falha ao ler arquivo: openpyxl={e1}, auto={e2}")
            
            print(f"✅ {len(df)} linhas encontradas no arquivo")
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
        current_tipo_zona = None
        
        # Processar cada linha do DataFrame
        for idx, row in df.iterrows():
            # Pular linha de cabeçalho
            if idx == 0:
                continue
                
            try:
                # Verificar se é uma nova zona
                suframa_col = row['SUFRAMA']
                if pd.notna(suframa_col) and str(suframa_col).strip():
                    current_tipo_zona = str(suframa_col).strip()
                    print(f"🏷️ Processando zona: {current_tipo_zona}")
                
                # Se não temos tipo de zona definido, usar a última conhecida
                if not current_tipo_zona:
                    current_tipo_zona = "ÁREAS DE LIVRE COMÉRCIO"  # Default para linhas sem tipo
                
                # Processar municípios nas colunas
                municipios_na_linha = []
                
                # Verificar colunas de municípios (pares: código, nome)
                colunas = ['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6']
                
                # Processar em pares (código, nome)
                for i in range(0, len(colunas), 2):
                    if i + 1 < len(colunas):
                        cod_col = colunas[i]
                        nome_col = colunas[i + 1]
                        
                        cod_mun = row.get(cod_col)
                        nome_mun = row.get(nome_col)
                        
                        # Validar se temos dados válidos
                        if pd.notna(cod_mun) and pd.notna(nome_mun):
                            cod_mun_clean = self._clean_string(str(int(cod_mun)))
                            nome_mun_clean = self._clean_string(str(nome_mun))
                            
                            if cod_mun_clean and nome_mun_clean:
                                municipio = {
                                    'cd_mun': cod_mun_clean,
                                    'nm_mun': nome_mun_clean,
                                    'tipo_zona': current_tipo_zona,
                                    'scraped_at': datetime.now().isoformat(),
                                    'source_url': self.url
                                }
                                municipios_na_linha.append(municipio)
                
                # Adicionar municípios processados
                processed_municipios.extend(municipios_na_linha)
                
                if municipios_na_linha:
                    print(f"   ✅ {len(municipios_na_linha)} municípios na linha {idx}")
                
            except Exception as e:
                print(f"⚠️ Erro ao processar linha {idx}: {e}")
                continue
        
        # Salvar dados processados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_file = f'data/processed/municipios_suframa_{timestamp}.json'
        
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
    
    def save_to_database(self, municipios: List[Dict[str, Any]]) -> int:
        """Salva os dados no banco PostgreSQL."""
        print("💾 Salvando no banco de dados...")
        
        # Criar tabelas se não existirem
        create_tables()
        
        saved_count = 0
        
        with SessionLocal() as db:
            try:
                # Primeiro, validar se temos dados para salvar
                if not municipios:
                    raise ValueError("Nenhum município foi processado para salvar")
                
                # Preparar todos os objetos primeiro (validação)
                municipios_objs = []
                for data in municipios:
                    municipio = MunicipioSuframa(
                        cd_mun=data['cd_mun'],
                        nm_mun=data['nm_mun'],
                        tipo_zona=data['tipo_zona'],
                        scraped_at=datetime.fromisoformat(data['scraped_at']),
                        source_url=data['source_url']
                    )
                    municipios_objs.append(municipio)
                
                # Se chegou até aqui, os dados estão válidos
                # Agora limpar a tabela existente
                print("🧹 Limpando tabela existente...")
                db.execute(text("TRUNCATE TABLE municipios_suframa RESTART IDENTITY CASCADE"))
                
                # Inserir dados novos
                print(f"📝 Inserindo {len(municipios_objs)} municípios...")
                for municipio in municipios_objs:
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
            total = db.execute(text("SELECT COUNT(*) FROM municipios_suframa")).scalar()
            
            # Contagem por tipo de zona
            zonas = db.execute(text("""
                SELECT tipo_zona, COUNT(*) as count 
                FROM municipios_suframa 
                GROUP BY tipo_zona 
                ORDER BY count DESC
            """)).fetchall()
            
            # Top municípios por zona
            zona_franca = db.execute(text("""
                SELECT nm_mun, cd_mun 
                FROM municipios_suframa 
                WHERE tipo_zona = 'ZONA FRANCA DE MANAUS'
                ORDER BY nm_mun
            """)).fetchall()
            
            areas_livre_comercio = db.execute(text("""
                SELECT nm_mun, cd_mun 
                FROM municipios_suframa 
                WHERE tipo_zona = 'ÁREAS DE LIVRE COMÉRCIO'
                ORDER BY nm_mun
            """)).fetchall()
            
            return {
                'total_municipios': total,
                'zonas': [{'tipo': row[0], 'count': row[1]} for row in zonas],
                'zona_franca_manaus': [{'nome': row[0], 'codigo': row[1]} for row in zona_franca],
                'areas_livre_comercio': [{'nome': row[0], 'codigo': row[1]} for row in areas_livre_comercio]
            }
    
    def run(self) -> Dict[str, Any]:
        """Executa o scraping completo."""
        print("🚀 Iniciando scraping de municípios SUFRAMA do IBGE...")
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
            cleanup_data_files('municipios_suframa')
            
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
            print(f"   📥 Linhas no arquivo: {len(df)}")
            print(f"   🔧 Municípios processados: {len(processed_data)}")
            print(f"   💾 Salvos no banco: {saved_count}")
            
            print(f"\n🏷️ Por tipo de zona:")
            for zona in stats['zonas']:
                print(f"   {zona['tipo']}: {zona['count']} municípios")
            
            print(f"\n🏗️ Zona Franca de Manaus:")
            for mun in stats['zona_franca_manaus']:
                print(f"   {mun['nome']} ({mun['codigo']})")
            
            print(f"\n🛒 Áreas de Livre Comércio:")
            for mun in stats['areas_livre_comercio']:
                print(f"   {mun['nome']} ({mun['codigo']})")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro durante o scraping: {e}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }

if __name__ == '__main__':
    scraper = MunicipiosSuframaIBGEScraper()
    result = scraper.run()
    
    if result['success']:
        print("\n🎉 Scraping concluído com sucesso!")
    else:
        print(f"\n💥 Scraping falhou: {result['error']}")
