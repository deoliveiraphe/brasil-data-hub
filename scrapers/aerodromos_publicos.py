"""
Scraper para aeródromos públicos da ANAC.
Usa dados JSON diretos da API de dados abertos.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

import requests
from sqlalchemy import text

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from database import SessionLocal, create_tables
from models import AerodromoPublico
from utils import cleanup_data_files


class AerodromosPublicosScraper:
    """Scraper específico para aeródromos públicos da ANAC."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*'
        })
        
        # URL direta do JSON de dados abertos
        self.url = 'https://sistemas.anac.gov.br/dadosabertos/Aerodromos/Aeródromos Públicos/Lista de aeródromos públicos/AerodromosPublicos.json'
        
        # Criar pastas se não existirem
        Path('data').mkdir(exist_ok=True)
        Path('data/raw').mkdir(exist_ok=True)
        Path('data/processed').mkdir(exist_ok=True)
    
    def fetch_data(self) -> List[Dict[str, Any]]:
        """Busca os dados JSON da ANAC."""
        print("🔍 Buscando dados de aeródromos públicos da ANAC...")
        
        try:
            response = self.session.get(self.url, timeout=30)
            response.raise_for_status()
            
            # Salvar dados brutos
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_file = f'data/raw/aerodromos_publicos_raw_{timestamp}.json'
            
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Parse JSON - lidar com BOM UTF-8
            try:
                data = response.json()
            except json.JSONDecodeError:
                # Tentar remover BOM se presente
                content = response.content.decode('utf-8-sig')
                data = json.loads(content)
            print(f"✅ {len(data)} aeródromos públicos encontrados")
            
            return data
            
        except requests.RequestException as e:
            print(f"❌ Erro ao buscar dados: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {e}")
            raise
    
    def process_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processa e limpa os dados brutos."""
        print("🔧 Processando dados...")
        
        processed_aerodromos = []
        
        for item in raw_data:
            try:
                # Extrair e limpar dados
                aerodromo = {
                    'codigo_oaci': self._clean_string(item.get('CódigoOACI')),
                    'ciad': self._clean_string(item.get('CIAD')),
                    'nome': self._clean_string(item.get('Nome')),
                    'municipio': self._clean_string(item.get('Município')),
                    'uf': self._clean_string(item.get('UF')),
                    'lat_geo_point': self._parse_coordinate(item.get('LatGeoPoint')),
                    'lon_geo_point': self._parse_coordinate(item.get('LonGeoPoint')),
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': self.url
                }
                
                # Validar dados obrigatórios
                if not aerodromo['nome'] or aerodromo['nome'].strip() == '':
                    print(f"⚠️ Aeródromo sem nome ignorado: {item.get('CIAD', 'SEM_CIAD')}")
                    continue
                
                processed_aerodromos.append(aerodromo)
                
            except Exception as e:
                print(f"⚠️ Erro ao processar item {item}: {e}")
                continue
        
        # Salvar dados processados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_file = f'data/processed/aerodromos_publicos_{timestamp}.json'
        
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(processed_aerodromos, f, ensure_ascii=False, indent=2)
        
        print(f"✅ {len(processed_aerodromos)} aeródromos processados")
        print(f"📁 Dados salvos em: {processed_file}")
        
        return processed_aerodromos
    
    def _clean_string(self, value: Any) -> Optional[str]:
        """Limpa e valida strings."""
        if value is None:
            return None
        
        cleaned = str(value).strip()
        return cleaned if cleaned and cleaned.upper() not in ['NULL', 'NONE', 'N/A', ''] else None
    
    def _parse_coordinate(self, coord_value: Any) -> Optional[float]:
        """Converte coordenada para float."""
        if coord_value is None:
            return None
        
        try:
            if isinstance(coord_value, (int, float)):
                return float(coord_value)
            
            # Se for string, tentar converter
            coord_str = str(coord_value).replace(',', '.').strip()
            if not coord_str or coord_str.upper() in ['NULL', 'NONE', 'N/A']:
                return None
                
            return float(coord_str)
            
        except (ValueError, TypeError):
            return None
    
    def save_to_database(self, aerodromos: List[Dict[str, Any]]) -> int:
        """Salva os dados no banco PostgreSQL."""
        print("💾 Salvando no banco de dados...")
        
        # Criar tabelas se não existirem
        create_tables()
        
        saved_count = 0
        
        with SessionLocal() as db:
            try:
                # Limpar tabela existente
                db.execute(text("TRUNCATE TABLE aerodromos_publicos RESTART IDENTITY CASCADE"))
                
                # Inserir dados
                for data in aerodromos:
                    aerodromo = AerodromoPublico(
                        codigo_oaci=data.get('codigo_oaci'),
                        ciad=data.get('ciad'),
                        nome=data['nome'],
                        municipio=data.get('municipio'),
                        uf=data.get('uf'),
                        latitude=data.get('lat_geo_point'),
                        longitude=data.get('lon_geo_point'),
                        scraped_at=datetime.fromisoformat(data['scraped_at']),
                        source_url=data['source_url']
                    )
                    db.add(aerodromo)
                    saved_count += 1
                
                db.commit()
                print(f"✅ {saved_count} aeródromos salvos no banco")
                
            except Exception as e:
                db.rollback()
                print(f"❌ Erro ao salvar no banco: {e}")
                raise
        
        return saved_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da tabela."""
        with SessionLocal() as db:
            # Contadores básicos
            total = db.execute(text("SELECT COUNT(*) FROM aerodromos_publicos")).scalar()
            
            com_oaci = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_publicos 
                WHERE codigo_oaci IS NOT NULL AND codigo_oaci != ''
            """)).scalar()
            
            com_ciad = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_publicos 
                WHERE ciad IS NOT NULL AND ciad != ''
            """)).scalar()
            
            com_coords = db.execute(text("""
                SELECT COUNT(*) FROM aerodromos_publicos 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)).scalar()
            
            # Top UFs
            top_ufs = db.execute(text("""
                SELECT uf, COUNT(*) as count 
                FROM aerodromos_publicos 
                WHERE uf IS NOT NULL 
                GROUP BY uf 
                ORDER BY count DESC 
                LIMIT 5
            """)).fetchall()
            
            return {
                'total_aerodromos': total,
                'com_codigo_oaci': com_oaci,
                'com_ciad': com_ciad,
                'com_coordenadas': com_coords,
                'sem_coordenadas': total - com_coords,
                'top_ufs': [{'uf': row[0], 'count': row[1]} for row in top_ufs]
            }
    
    def run(self) -> Dict[str, Any]:
        """Executa o scraping completo."""
        print("🚀 Iniciando scraping de aeródromos públicos...")
        start_time = time.time()
        
        try:
            # 1. Buscar dados
            raw_data = self.fetch_data()
            
            # 2. Processar dados
            processed_data = self.process_data(raw_data)
            
            # 3. Salvar no banco
            saved_count = self.save_to_database(processed_data)
            
            # 4. Estatísticas
            stats = self.get_stats()
            
            # 5. Limpeza de arquivos antigos
            cleanup_data_files('aerodromos_publicos')
            
            elapsed_time = time.time() - start_time
            
            result = {
                'success': True,
                'raw_count': len(raw_data),
                'processed_count': len(processed_data),
                'saved_count': saved_count,
                'elapsed_time': elapsed_time,
                'stats': stats
            }
            
            print(f"\n📊 Resumo do scraping:")
            print(f"   ⏱️ Tempo: {elapsed_time:.2f}s")
            print(f"   📥 Dados brutos: {len(raw_data)}")
            print(f"   🔧 Processados: {len(processed_data)}")
            print(f"   💾 Salvos no banco: {saved_count}")
            print(f"   📍 Com coordenadas: {stats['com_coordenadas']}")
            print(f"   🏷️ Com código OACI: {stats['com_codigo_oaci']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro durante o scraping: {e}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }


if __name__ == '__main__':
    scraper = AerodromosPublicosScraper()
    result = scraper.run()
    
    if result['success']:
        print("\n🎉 Scraping concluído com sucesso!")
    else:
        print(f"\n💥 Scraping falhou: {result['error']}")
