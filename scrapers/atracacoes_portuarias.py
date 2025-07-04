"""
Scraper para dados de atracações portuárias da ANTAQ.
Baixa e processa dados de arquivo ZIP/TXT com dados de atracações.
"""

import csv
import json
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import io
import re

import requests
from sqlalchemy import text

# Adicionar o diretório pai ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from database import SessionLocal, create_tables
from models import AtracacaoPortuaria
from utils import cleanup_data_files

class AtracacoesPortuariasANTAQScraper:
    """Scraper específico para dados de atracações portuárias da ANTAQ."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/zip, application/octet-stream, */*'
        })
        
        # URL do arquivo ZIP da ANTAQ
        self.url = 'https://web3.antaq.gov.br/ea/txt/2025Atracacao.zip'
        
        # Criar pastas se não existirem
        Path('data').mkdir(exist_ok=True)
        Path('data/raw').mkdir(exist_ok=True)
        Path('data/processed').mkdir(exist_ok=True)
    
    def fetch_data(self) -> str:
        """Baixa e extrai o arquivo ZIP da ANTAQ."""
        print("🔍 Buscando dados de atracações portuárias da ANTAQ...")
        
        try:
            response = self.session.get(self.url, timeout=120)
            response.raise_for_status()
            
            # Salvar arquivo ZIP bruto
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            raw_zip_file = f'data/raw/atracacoes_portuarias_raw_{timestamp}.zip'
            
            with open(raw_zip_file, 'wb') as f:
                f.write(response.content)
            
            print(f"📁 Arquivo ZIP salvo em: {raw_zip_file}")
            
            # Extrair arquivo TXT do ZIP
            with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
                # Listar arquivos no ZIP
                zip_files = zip_ref.namelist()
                print(f"🔍 Arquivos no ZIP: {zip_files}")
                
                # Encontrar o arquivo TXT
                txt_files = [f for f in zip_files if f.endswith('.txt')]
                if not txt_files:
                    raise Exception("Nenhum arquivo TXT encontrado no ZIP")
                
                txt_filename = txt_files[0]
                print(f"📄 Extraindo arquivo: {txt_filename}")
                
                # Extrair conteúdo do TXT
                with zip_ref.open(txt_filename) as txt_file:
                    txt_content = txt_file.read().decode('utf-8-sig')  # Remove BOM se presente
                
                # Salvar TXT extraído
                raw_txt_file = f'data/raw/atracacoes_portuarias_raw_{timestamp}.txt'
                with open(raw_txt_file, 'w', encoding='utf-8') as f:
                    f.write(txt_content)
                
                print(f"📄 Arquivo TXT extraído para: {raw_txt_file}")
                
                return txt_content
            
        except requests.RequestException as e:
            print(f"❌ Erro ao buscar dados: {e}")
            raise
        except Exception as e:
            print(f"❌ Erro ao processar ZIP/TXT: {e}")
            raise
    
    def process_data(self, txt_content: str) -> List[Dict[str, Any]]:
        """Processa e limpa os dados do arquivo TXT."""
        print("🔧 Processando dados...")
        
        processed_atracacoes = []
        
        # Converter TXT para CSV (já está delimitado por ponto e vírgula)
        csv_reader = csv.DictReader(io.StringIO(txt_content), delimiter=';')
        
        # Mapear nomes das colunas esperadas
        expected_columns = [
            'IDAtracacao', 'CDTUP', 'IDBerco', 'Berço', 'Porto Atracação', 'Coordenadas',
            'Apelido Instalação Portuária', 'Complexo Portuário', 'Tipo da Autoridade Portuária',
            'Data Atracação', 'Data Chegada', 'Data Desatracação', 'Data Início Operação',
            'Data Término Operação', 'Ano', 'Mes', 'Tipo de Operação', 'Tipo de Navegação da Atracação',
            'Nacionalidade do Armador', 'FlagMCOperacaoAtracacao', 'Terminal', 'Município', 'UF',
            'SGUF', 'Região Geográfica', 'Região Hidrográfica', 'Instalação Portuária em Rio',
            'Nº da Capitania', 'Nº do IMO'
        ]
        
        print(f"🔍 Colunas encontradas: {csv_reader.fieldnames}")
        
        total_rows = 0
        for idx, row in enumerate(csv_reader):
            total_rows += 1
            
            try:
                # Extrair e limpar dados
                atracacao = {
                    'id_atracacao': self._clean_string(row.get('IDAtracacao')),
                    'cdtup': self._clean_string(row.get('CDTUP')),
                    'id_berco': self._clean_string(row.get('IDBerco')),
                    'berco': self._clean_string(row.get('Berço')),
                    'porto_atracacao': self._clean_string(row.get('Porto Atracação')),
                    'coordenadas': self._clean_string(row.get('Coordenadas')),
                    'apelido_instalacao': self._clean_string(row.get('Apelido Instalação Portuária')),
                    'complexo_portuario': self._clean_string(row.get('Complexo Portuário')),
                    'tipo_autoridade': self._clean_string(row.get('Tipo da Autoridade Portuária')),
                    'data_atracacao': self._parse_datetime(row.get('Data Atracação')),
                    'data_chegada': self._parse_datetime(row.get('Data Chegada')),
                    'data_desatracacao': self._parse_datetime(row.get('Data Desatracação')),
                    'data_inicio_operacao': self._parse_datetime(row.get('Data Início Operação')),
                    'data_termino_operacao': self._parse_datetime(row.get('Data Término Operação')),
                    'ano': self._parse_int(row.get('Ano')),
                    'mes': self._clean_string(row.get('Mes')),
                    'tipo_operacao': self._clean_string(row.get('Tipo de Operação')),
                    'tipo_navegacao': self._clean_string(row.get('Tipo de Navegação da Atracação')),
                    'nacionalidade_armador': self._clean_string(row.get('Nacionalidade do Armador')),
                    'flag_mc_operacao': self._clean_string(row.get('FlagMCOperacaoAtracacao')),
                    'terminal': self._clean_string(row.get('Terminal')),
                    'municipio': self._clean_string(row.get('Município')),
                    'uf': self._clean_string(row.get('UF')),
                    'sguf': self._clean_string(row.get('SGUF')),
                    'regiao_geografica': self._clean_string(row.get('Região Geográfica')),
                    'regiao_hidrografica': self._clean_string(row.get('Região Hidrográfica')),
                    'instalacao_em_rio': self._clean_string(row.get('Instalação Portuária em Rio')),
                    'numero_capitania': self._clean_string(row.get('Nº da Capitania')),
                    'numero_imo': self._clean_string(row.get('Nº do IMO')),
                    'scraped_at': datetime.now().isoformat(),
                    'source_url': self.url
                }
                
                # Extrair coordenadas
                lat, lon = self._parse_coordinates(atracacao['coordenadas'])
                atracacao['latitude'] = lat
                atracacao['longitude'] = lon
                
                # Validar dados obrigatórios
                if not atracacao['id_atracacao']:
                    print(f"⚠️ Atracação sem ID ignorada na linha {idx + 2}")
                    continue
                
                processed_atracacoes.append(atracacao)
                
                if (idx + 1) % 5000 == 0:
                    print(f"   📊 Processadas {idx + 1} linhas...")
                
            except Exception as e:
                print(f"⚠️ Erro ao processar linha {idx + 2}: {e}")
                continue
        
        # Salvar dados processados
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        processed_file = f'data/processed/atracacoes_portuarias_{timestamp}.json'
        
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(processed_atracacoes, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"✅ {len(processed_atracacoes)} atracações processadas de {total_rows} linhas totais")
        print(f"📁 Dados salvos em: {processed_file}")
        
        return processed_atracacoes
    
    def _clean_string(self, value: Any) -> Optional[str]:
        """Limpa e valida strings."""
        if value is None or str(value).strip() == '':
            return None
        
        cleaned = str(value).strip()
        return cleaned if cleaned and cleaned.upper() not in ['NULL', 'NONE', 'N/A', 'NAN'] else None
    
    def _parse_int(self, value: Any) -> Optional[int]:
        """Converte valor para int."""
        if value is None:
            return None
        
        try:
            return int(str(value).strip())
        except (ValueError, TypeError):
            return None
    
    def _parse_datetime(self, value: Any) -> Optional[str]:
        """Converte string de data/hora para formato ISO."""
        if not value or str(value).strip() == '':
            return None
        
        try:
            # Formato esperado: 31/01/2025 08:15:00
            date_str = str(value).strip()
            if '/' in date_str and ' ' in date_str:
                date_part, time_part = date_str.split(' ', 1)
                day, month, year = date_part.split('/')
                
                # Reformat para ISO
                iso_datetime = f"{year}-{month.zfill(2)}-{day.zfill(2)}T{time_part}"
                return iso_datetime
            
            return None
            
        except (ValueError, TypeError, AttributeError):
            return None
    
    def _parse_coordinates(self, coords_str: Optional[str]) -> tuple[Optional[float], Optional[float]]:
        """Extrai latitude e longitude de string de coordenadas."""
        if not coords_str:
            return None, None
        
        try:
            # Formato esperado: -48.497777,-1.445278
            coords_clean = coords_str.strip()
            if ',' in coords_clean:
                lon_str, lat_str = coords_clean.split(',', 1)
                lon = float(lon_str.strip())
                lat = float(lat_str.strip())
                return lat, lon
            
            return None, None
            
        except (ValueError, TypeError, AttributeError):
            return None, None
    
    def save_to_database(self, atracacoes: List[Dict[str, Any]]) -> int:
        """Salva os dados no banco PostgreSQL."""
        print("💾 Salvando no banco de dados...")
        
        # Criar tabelas se não existirem
        create_tables()
        
        saved_count = 0
        
        with SessionLocal() as db:
            try:
                # Primeiro, validar se temos dados para salvar
                if not atracacoes:
                    raise ValueError("Nenhuma atracação foi processada para salvar")
                
                print(f"🧹 Limpando tabela existente...")
                db.execute(text("TRUNCATE TABLE atracacoes_portuarias RESTART IDENTITY CASCADE"))
                
                print(f"📝 Inserindo {len(atracacoes)} atracações...")
                batch_size = 1000
                
                for i in range(0, len(atracacoes), batch_size):
                    batch = atracacoes[i:i + batch_size]
                    
                    for data in batch:
                        atracacao = AtracacaoPortuaria(
                            id_atracacao=data['id_atracacao'],
                            cdtup=data.get('cdtup'),
                            id_berco=data.get('id_berco'),
                            berco=data.get('berco'),
                            porto_atracacao=data.get('porto_atracacao'),
                            coordenadas=data.get('coordenadas'),
                            latitude=data.get('latitude'),
                            longitude=data.get('longitude'),
                            apelido_instalacao=data.get('apelido_instalacao'),
                            complexo_portuario=data.get('complexo_portuario'),
                            tipo_autoridade=data.get('tipo_autoridade'),
                            data_atracacao=datetime.fromisoformat(data['data_atracacao']) if data.get('data_atracacao') else None,
                            data_chegada=datetime.fromisoformat(data['data_chegada']) if data.get('data_chegada') else None,
                            data_desatracacao=datetime.fromisoformat(data['data_desatracacao']) if data.get('data_desatracacao') else None,
                            data_inicio_operacao=datetime.fromisoformat(data['data_inicio_operacao']) if data.get('data_inicio_operacao') else None,
                            data_termino_operacao=datetime.fromisoformat(data['data_termino_operacao']) if data.get('data_termino_operacao') else None,
                            ano=data.get('ano'),
                            mes=data.get('mes'),
                            tipo_operacao=data.get('tipo_operacao'),
                            tipo_navegacao=data.get('tipo_navegacao'),
                            nacionalidade_armador=data.get('nacionalidade_armador'),
                            flag_mc_operacao=data.get('flag_mc_operacao'),
                            terminal=data.get('terminal'),
                            municipio=data.get('municipio'),
                            uf=data.get('uf'),
                            sguf=data.get('sguf'),
                            regiao_geografica=data.get('regiao_geografica'),
                            regiao_hidrografica=data.get('regiao_hidrografica'),
                            instalacao_em_rio=data.get('instalacao_em_rio'),
                            numero_capitania=data.get('numero_capitania'),
                            numero_imo=data.get('numero_imo'),
                            scraped_at=datetime.fromisoformat(data['scraped_at']),
                            source_url=data['source_url']
                        )
                        db.add(atracacao)
                        saved_count += 1
                    
                    # Commit em lotes
                    db.commit()
                    print(f"   💾 Salvos {min(i + batch_size, len(atracacoes))} de {len(atracacoes)} registros...")
                
                print(f"✅ {saved_count} atracações salvas no banco")
                
            except Exception as e:
                db.rollback()
                print(f"❌ Erro ao salvar no banco: {e}")
                raise
        
        return saved_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas da tabela."""
        with SessionLocal() as db:
            # Contadores básicos
            total = db.execute(text("SELECT COUNT(*) FROM atracacoes_portuarias")).scalar()
            
            # Com coordenadas
            com_coordenadas = db.execute(text("""
                SELECT COUNT(*) FROM atracacoes_portuarias 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)).scalar()
            
            # Por ano
            por_ano = db.execute(text("""
                SELECT ano, COUNT(*) as count 
                FROM atracacoes_portuarias 
                WHERE ano IS NOT NULL 
                GROUP BY ano 
                ORDER BY ano DESC
            """)).fetchall()
            
            # Top portos
            top_portos = db.execute(text("""
                SELECT porto_atracacao, COUNT(*) as count 
                FROM atracacoes_portuarias 
                WHERE porto_atracacao IS NOT NULL 
                GROUP BY porto_atracacao 
                ORDER BY count DESC 
                LIMIT 10
            """)).fetchall()
            
            # Top UFs
            top_ufs = db.execute(text("""
                SELECT sguf, COUNT(*) as count 
                FROM atracacoes_portuarias 
                WHERE sguf IS NOT NULL 
                GROUP BY sguf 
                ORDER BY count DESC 
                LIMIT 10
            """)).fetchall()
            
            # Tipos de navegação
            tipos_navegacao = db.execute(text("""
                SELECT tipo_navegacao, COUNT(*) as count 
                FROM atracacoes_portuarias 
                WHERE tipo_navegacao IS NOT NULL 
                GROUP BY tipo_navegacao 
                ORDER BY count DESC
            """)).fetchall()
            
            return {
                'total_atracacoes': total,
                'com_coordenadas': com_coordenadas,
                'por_ano': [{'ano': row[0], 'count': row[1]} for row in por_ano],
                'top_portos': [{'porto': row[0], 'count': row[1]} for row in top_portos],
                'top_ufs': [{'uf': row[0], 'count': row[1]} for row in top_ufs],
                'tipos_navegacao': [{'tipo': row[0], 'count': row[1]} for row in tipos_navegacao]
            }
    
    def run(self) -> Dict[str, Any]:
        """Executa o scraping completo."""
        print("🚀 Iniciando scraping de atracações portuárias da ANTAQ...")
        start_time = time.time()
        
        try:
            # 1. Buscar dados
            txt_content = self.fetch_data()
            
            # 2. Processar dados
            processed_data = self.process_data(txt_content)
            
            # 3. Salvar no banco
            saved_count = self.save_to_database(processed_data)
            
            # 4. Estatísticas
            stats = self.get_stats()
            
            # 5. Limpeza de arquivos antigos
            cleanup_data_files('atracacoes_portuarias')
            
            elapsed_time = time.time() - start_time
            
            result = {
                'success': True,
                'processed_count': len(processed_data),
                'saved_count': saved_count,
                'elapsed_time': elapsed_time,
                'stats': stats
            }
            
            print(f"\n📊 Resumo do scraping:")
            print(f"   ⏱️ Tempo: {elapsed_time:.2f}s")
            print(f"   🔧 Atracações processadas: {len(processed_data)}")
            print(f"   💾 Salvas no banco: {saved_count}")
            print(f"   📍 Com coordenadas: {stats['com_coordenadas']}")
            
            print(f"\n📅 Por ano:")
            for ano_data in stats['por_ano'][:5]:  # Top 5 anos
                print(f"   {ano_data['ano']}: {ano_data['count']} atracações")
            
            print(f"\n🏗️ Top portos:")
            for porto in stats['top_portos'][:5]:  # Top 5 portos
                print(f"   {porto['porto']}: {porto['count']} atracações")
            
            return result
            
        except Exception as e:
            print(f"❌ Erro durante o scraping: {e}")
            return {
                'success': False,
                'error': str(e),
                'elapsed_time': time.time() - start_time
            }

if __name__ == '__main__':
    scraper = AtracacoesPortuariasANTAQScraper()
    result = scraper.run()
    
    if result['success']:
        print("\n🎉 Scraping concluído com sucesso!")
    else:
        print(f"\n💥 Scraping falhou: {result['error']}")
