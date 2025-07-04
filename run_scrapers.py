#!/usr/bin/env python3
"""
Script principal para executar todos os scrapers do Brasil Data Hub.

Este script:
1. Limpa todas as tabelas do banco de dados
2. Executa todos os scrapers em sequência
3. Gera relatório final com estatísticas
4. Salva logs detalhados de execução

Usage:
    python run_scrapers.py                    # Executa todos os scrapers
    python run_scrapers.py --scraper private # Executa apenas aeródromos privados
    python run_scrapers.py --scraper public  # Executa apenas aeródromos públicos
    python run_scrapers.py --no-clean        # Executa sem limpar as tabelas
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from sqlalchemy import text

# Adicionar pasta scrapers ao path
sys.path.append(str(Path(__file__).parent))

from database import SessionLocal, create_tables, get_stats
from scrapers.aerodromos_privados import AerodromosPrivadosScraper
from scrapers.aerodromos_publicos import AerodromosPublicosScraper
from scrapers.municipios_maritimos import MunicipiosMaritimosIBGEScraper
from scrapers.municipios_fronteira import MunicipiosFronteiraIBGEScraper
from scrapers.municipios_suframa import MunicipiosSuframaIBGEScraper
from scrapers.atracacoes_portuarias import AtracacoesPortuariasANTAQScraper
from process_representacoes_fiscais import main as processar_representacoes_fiscais
from utils import cleanup_all_data_files


class BrasilDataHubScrapersManager:
    """Gerenciador principal para todos os scrapers do Brasil Data Hub."""
    
    def __init__(self):
        """Inicializa o gerenciador com todos os scrapers disponíveis."""
        self.scrapers = {
            'private': {
                'name': 'Aeródromos Privados',
                'scraper': AerodromosPrivadosScraper(),
                'description': 'Aeródromos privados registrados na ANAC'
            },
            'public': {
                'name': 'Aeródromos Públicos', 
                'scraper': AerodromosPublicosScraper(),
                'description': 'Aeródromos públicos registrados na ANAC'
            },
            'maritimos': {
                'name': 'Municípios Marítimos',
                'scraper': MunicipiosMaritimosIBGEScraper(),
                'description': 'Municípios defrontantes com o mar - IBGE'
            },
            'fronteira': {
                'name': 'Municípios de Fronteira',
                'scraper': MunicipiosFronteiraIBGEScraper(),
                'description': 'Municípios da faixa de fronteira e cidades gêmeas - IBGE'
            },
            'suframa': {
                'name': 'Municípios SUFRAMA',
                'scraper': MunicipiosSuframaIBGEScraper(),
                'description': 'Municípios das Zonas Fiscais Especiais da SUFRAMA - IBGE'
            },
            'portos': {
                'name': 'Atracações Portuárias',
                'scraper': AtracacoesPortuariasANTAQScraper(),
                'description': 'Dados de atracações portuárias - ANTAQ'
            },
            'representacoes_fiscais_scraper': {
                'name': 'Representações Fiscais (Scraper)',
                'scraper': None,  # Será tratado de forma especial
                'description': 'Coleta de dados de representações fiscais do Power BI'
            },
            'representacoes_fiscais_process': {
                'name': 'Representações Fiscais (Processamento)',
                'scraper': None,  # Será tratado de forma especial
                'description': 'Processamento de representações fiscais do CSV para o banco'
            }
        }
        
        # Criar pasta de logs se não existir
        Path('logs').mkdir(exist_ok=True)
    
    def create_tables_if_needed(self) -> bool:
        """Cria tabelas se não existirem (sem limpá-las)."""
        print("🔧 Verificando/criando tabelas no banco de dados...")
        
        try:
            # Criar tabelas se não existirem
            create_tables()
            print("✅ Tabelas verificadas/criadas")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao verificar/criar tabelas: {e}")
            return False
    
    def run_single_scraper(self, scraper_key: str) -> Dict[str, Any]:
        """Executa um único scraper."""
        if scraper_key not in self.scrapers:
            available = ', '.join(self.scrapers.keys())
            raise ValueError(f"Scraper '{scraper_key}' não encontrado. Disponíveis: {available}")
        
        scraper_info = self.scrapers[scraper_key]
        print(f"\n{'='*70}")
        print(f"🎯 Executando: {scraper_info['name']}")
        print(f"📄 Descrição: {scraper_info['description']}")
        print(f"{'='*70}")
        
        start_time = time.time()
        
        try:
            if scraper_key == 'representacoes_fiscais_scraper':
                # Executar o scraper de representações fiscais
                from scrapers.representacoes_fiscais import executar_estrategias_avancadas
                print(f"\n{'='*70}")
                print(f"🎯 Executando: Representações Fiscais (Scraper)")
                print(f"📄 Descrição: Coleta de dados de representações fiscais do Power BI")
                print(f"{'='*70}")
                start_time = time.time()
                try:
                    arquivo_csv = executar_estrategias_avancadas()
                    result = {
                        'success': True,
                        'scraper_name': 'Representações Fiscais (Scraper)',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time,
                        'csv_file': arquivo_csv
                    }
                    print(f"✅ Representações Fiscais (Scraper): Concluído com sucesso!")
                except Exception as e:
                    result = {
                        'success': False,
                        'error': str(e),
                        'scraper_name': 'Representações Fiscais (Scraper)',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time
                    }
                    print(f"❌ Representações Fiscais (Scraper): Falhou - {e}")
                return result
            elif scraper_key == 'representacoes_fiscais_process':
                # Executar o processamento do CSV
                print(f"\n{'='*70}")
                print(f"🎯 Executando: Representações Fiscais (Processamento)")
                print(f"📄 Descrição: Processamento de representações fiscais do CSV para o banco")
                print(f"{'='*70}")
                start_time = time.time()
                try:
                    processar_representacoes_fiscais()
                    result = {
                        'success': True,
                        'scraper_name': 'Representações Fiscais (Processamento)',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time
                    }
                    print(f"✅ Representações Fiscais (Processamento): Concluído com sucesso!")
                except Exception as e:
                    result = {
                        'success': False,
                        'error': str(e),
                        'scraper_name': 'Representações Fiscais (Processamento)',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time
                    }
                    print(f"❌ Representações Fiscais (Processamento): Falhou - {e}")
                return result
            elif scraper_key == 'representacoes_fiscais':
                print(f"\n{'='*70}")
                print(f"🎯 Executando: Representações Fiscais")
                print(f"📄 Descrição: Processamento de representações fiscais do CSV para o banco")
                print(f"{'='*70}")
                start_time = time.time()
                try:
                    processar_representacoes_fiscais()
                    result = {
                        'success': True,
                        'scraper_name': 'Representações Fiscais',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time
                    }
                    print(f"✅ Representações Fiscais: Concluído com sucesso!")
                except Exception as e:
                    result = {
                        'success': False,
                        'error': str(e),
                        'scraper_name': 'Representações Fiscais',
                        'scraper_key': scraper_key,
                        'execution_time': time.time() - start_time
                    }
                    print(f"❌ Representações Fiscais: Falhou - {e}")
                return result
            else:
                result = scraper_info['scraper'].run()
                result['scraper_name'] = scraper_info['name']
                result['scraper_key'] = scraper_key
                result['execution_time'] = time.time() - start_time
                
                if result['success']:
                    print(f"✅ {scraper_info['name']}: Concluído com sucesso!")
                else:
                    print(f"❌ {scraper_info['name']}: Falhou - {result.get('error', 'Erro desconhecido')}")
                
                return result
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e),
                'scraper_name': scraper_info['name'],
                'scraper_key': scraper_key,
                'execution_time': time.time() - start_time
            }
            print(f"💥 {scraper_info['name']}: Exceção fatal - {e}")
            return error_result
    
    def run_all_scrapers(self, clean_tables: bool = True) -> Dict[str, Any]:
        """Executa todos os scrapers em sequência."""
        print("🚀 Iniciando execução completa dos scrapers do Brasil Data Hub...")
        print(f"📅 Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        start_time = time.time()
        execution_log = {
            'start_time': datetime.now().isoformat(),
            'clean_tables_requested': clean_tables,
            'scrapers_executed': [],
            'summary': {}
        }
        
        # 1. Verificar/criar tabelas (sem limpar)
        if clean_tables:
            print("📋 Modo de limpeza ativado - cada scraper limpará sua própria tabela após validar os novos dados")
        else:
            print("⏭️ Modo sem limpeza - novos dados serão adicionados às tabelas existentes")
        
        # Criar tabelas se necessário
        tables_success = self.create_tables_if_needed()
        execution_log['tables_success'] = tables_success
        
        if not tables_success:
            print("⚠️ Falha ao verificar/criar tabelas. Continuando mesmo assim...")
        
        # 2. Executar scrapers
        results = {}
        successful_scrapers = 0
        failed_scrapers = 0
        
        for scraper_key in list(self.scrapers.keys()) + ['representacoes_fiscais_scraper', 'representacoes_fiscais_process']:
            try:
                result = self.run_single_scraper(scraper_key)
                results[scraper_key] = result
                execution_log['scrapers_executed'].append(result)
                
                if result['success']:
                    successful_scrapers += 1
                else:
                    failed_scrapers += 1
                    
            except Exception as e:
                failed_scrapers += 1
                error_result = {
                    'success': False,
                    'error': str(e),
                    'scraper_key': scraper_key,
                    'execution_time': 0
                }
                results[scraper_key] = error_result
                execution_log['scrapers_executed'].append(error_result)
                print(f"💥 Erro crítico no scraper {scraper_key}: {e}")
        
        # 3. Estatísticas finais
        total_execution_time = time.time() - start_time
        
        try:
            final_database_stats = get_stats()
        except Exception as e:
            print(f"⚠️ Erro ao obter estatísticas finais do banco: {e}")
            final_database_stats = {}
        
        # 4. Compilar resumo
        total_scrapers = len(self.scrapers) + 2  # +2 para os scrapers de representações fiscais
        execution_summary = {
            'total_scrapers': total_scrapers,
            'successful_scrapers': successful_scrapers,
            'failed_scrapers': failed_scrapers,
            'total_execution_time': total_execution_time,
            'database_stats': final_database_stats,
            'individual_results': results,
            'end_time': datetime.now().isoformat()
        }
        
        execution_log['summary'] = execution_summary
        
        # 5. Salvar log de execução
        self._save_execution_log(execution_log)
        
        # 6. Limpeza final de arquivos brutos
        self._cleanup_raw_files()
        
        # 7. Exibir relatório final
        self._print_final_report(execution_summary)
        
        return execution_summary
    
    def _save_execution_log(self, execution_log: Dict[str, Any]) -> None:
        """Salva o log detalhado da execução."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_file = f'logs/scrapers_execution_{timestamp}.json'
            
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(execution_log, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"📋 Log de execução salvo em: {log_file}")
            
        except Exception as e:
            print(f"⚠️ Erro ao salvar log de execução: {e}")
    
    def _cleanup_raw_files(self) -> None:
        """Remove todos os arquivos brutos da pasta data/raw após execução completa."""
        print(f"\n🗑️ Limpando arquivos brutos...")
        
        try:
            raw_path = Path('data/raw')
            if not raw_path.exists():
                print("   📁 Pasta data/raw não existe")
                return
            
            removed_count = 0
            total_size = 0
            
            # Percorrer todos os arquivos na pasta raw
            for file_path in raw_path.iterdir():
                if file_path.is_file() and not file_path.name.startswith('.'):
                    try:
                        file_size = file_path.stat().st_size
                        total_size += file_size
                        file_path.unlink()
                        removed_count += 1
                        print(f"   🗑️ Removido: {file_path.name} ({file_size:,} bytes)")
                    except Exception as e:
                        print(f"   ⚠️ Erro ao remover {file_path.name}: {e}")
            
            if removed_count > 0:
                total_mb = total_size / (1024 * 1024)
                print(f"✅ Limpeza concluída: {removed_count} arquivos removidos ({total_mb:.2f} MB)")
            else:
                print("   📁 Nenhum arquivo bruto encontrado para remoção")
                
        except Exception as e:
            print(f"❌ Erro durante limpeza de arquivos brutos: {e}")
    
    def _print_final_report(self, summary: Dict[str, Any]) -> None:
        """Imprime o relatório final da execução."""
        print(f"\n{'='*70}")
        print("📈 RELATÓRIO FINAL DE EXECUÇÃO")
        print(f"{'='*70}")
        
        # Tempo e status geral
        print(f"⏱️ Tempo total de execução: {summary['total_execution_time']:.2f} segundos")
        print(f"✅ Scrapers bem-sucedidos: {summary['successful_scrapers']}/{summary['total_scrapers']}")
        print(f"❌ Scrapers com falha: {summary['failed_scrapers']}/{summary['total_scrapers']}")
        
        # Resultados individuais
        print(f"\n📊 Resultados por Scraper:")
        for scraper_key, result in summary['individual_results'].items():
            # Tratar scrapers especiais de representações fiscais
            if scraper_key in ['representacoes_fiscais_scraper', 'representacoes_fiscais_process']:
                scraper_name = result.get('scraper_name', scraper_key)
            else:
                scraper_name = self.scrapers.get(scraper_key, {}).get('name', scraper_key)
            
            status = "✅ SUCESSO" if result['success'] else "❌ FALHA"
            execution_time = result.get('execution_time', 0)
            
            print(f"   {status} {scraper_name} ({execution_time:.2f}s)")
            
            if result['success'] and 'stats' in result:
                stats = result['stats']
                
                # Estatísticas específicas por tipo de scraper
                if scraper_key in ['private', 'public']:
                    # Aeródromos - mostrar coordenadas e código OACI
                    print(f"      📊 Total: {stats.get('total_aerodromos', 0)}")
                    print(f"      📍 Com coordenadas: {stats.get('com_coordenadas', 0)}")
                    print(f"      🏷️ Com código OACI: {stats.get('com_codigo_oaci', 0)}")
                elif scraper_key == 'maritimos':
                    # Municípios marítimos - mostrar total e área
                    total_mun = stats.get('total_municipios', 0)
                    area_total = stats.get('area_total_km2', 0)
                    print(f"      📊 Total: {total_mun} municípios")
                    if area_total > 0:
                        print(f"      📐 Área total: {area_total:.2f} km²")
                elif scraper_key == 'fronteira':
                    # Municípios de fronteira - mostrar total, cidades gêmeas, etc.
                    total_mun = stats.get('total_municipios', 0)
                    cidades_gemeas = stats.get('cidades_gemeas', 0)
                    toca_limite = stats.get('toca_limite', 0)
                    print(f"      📊 Total: {total_mun} municípios")
                    print(f"      🤝 Cidades gêmeas: {cidades_gemeas}")
                    print(f"      🔗 Tocam limite: {toca_limite}")
                elif scraper_key == 'suframa':
                    # Municípios SUFRAMA - mostrar total e distribuição por zona
                    total_mun = stats.get('total_municipios', 0)
                    zonas = stats.get('zonas', [])
                    print(f"      📊 Total: {total_mun} municípios")
                    for zona in zonas:
                        if zona['tipo'] == 'ZONA FRANCA DE MANAUS':
                            print(f"      🏗️ Zona Franca: {zona['count']}")
                        elif zona['tipo'] == 'ÁREAS DE LIVRE COMÉRCIO':
                            print(f"      🛒 Áreas Livre Comércio: {zona['count']}")
                elif scraper_key == 'portos':
                    # Atracações portuárias - mostrar total, coordenadas e top portos
                    total_atr = stats.get('total_atracacoes', 0)
                    com_coords = stats.get('com_coordenadas', 0)
                    print(f"      📊 Total: {total_atr} atracações")
                    print(f"      📍 Com coordenadas: {com_coords}")
                    top_portos = stats.get('top_portos', [])
                    if top_portos:
                        print(f"      🏗️ Top porto: {top_portos[0]['porto']}")
                elif scraper_key in ['representacoes_fiscais_scraper', 'representacoes_fiscais_process']:
                    # Representações fiscais - mostrar informações específicas
                    if 'csv_file' in result:
                        print(f"      📄 Arquivo CSV: {result['csv_file']}")
                    if 'total_registros' in stats:
                        print(f"      📊 Total: {stats.get('total_registros', 0)} registros")
            elif not result['success']:
                print(f"      💥 Erro: {result.get('error', 'Desconhecido')}")
        
        # Estatísticas do banco de dados
        if summary['database_stats']:
            print(f"\n🗄️ Estatísticas do Banco de Dados:")
            db_stats = summary['database_stats']
            
            if 'aerodromos_privados' in db_stats:
                priv_stats = db_stats['aerodromos_privados']
                print(f"   🏠 Aeródromos Privados: {priv_stats['total']}")
                print(f"      📍 Com coordenadas: {priv_stats['com_coordenadas']}")
                print(f"      🏷️ Com código OACI: {priv_stats['com_codigo_oaci']}")
            
            if 'aerodromos_publicos' in db_stats:
                pub_stats = db_stats['aerodromos_publicos']
                print(f"   🏛️ Aeródromos Públicos: {pub_stats['total']}")
                print(f"      📍 Com coordenadas: {pub_stats['com_coordenadas']}")
                print(f"      🏷️ Com código OACI: {pub_stats['com_codigo_oaci']}")
            
            if 'municipios_maritimos' in db_stats:
                mar_stats = db_stats['municipios_maritimos']
                print(f"   🌊 Municípios Marítimos: {mar_stats['total']}")
            
            if 'municipios_fronteira' in db_stats:
                front_stats = db_stats['municipios_fronteira']
                print(f"   🏛️ Municípios Fronteira: {front_stats['total']}")
            
            if 'municipios_suframa' in db_stats:
                suframa_stats = db_stats['municipios_suframa']
                print(f"   🏗️ Municípios SUFRAMA: {suframa_stats['total']}")
        
        # Status final
        if summary['successful_scrapers'] == summary['total_scrapers']:
            print(f"\n🎉 TODOS OS SCRAPERS EXECUTADOS COM SUCESSO!")
        elif summary['successful_scrapers'] > 0:
            print(f"\n⚠️ EXECUÇÃO PARCIALMENTE BEM-SUCEDIDA")
        else:
            print(f"\n💥 FALHA COMPLETA NA EXECUÇÃO")
        
        print(f"{'='*70}")


def main():
    """Função principal com interface de linha de comando."""
    parser = argparse.ArgumentParser(
        description='Executor de scrapers do Brasil Data Hub',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python run_scrapers.py                                         # Executa todos os scrapers
  python run_scrapers.py --scraper private                       # Apenas aeródromos privados
  python run_scrapers.py --scraper public                        # Apenas aeródromos públicos
  python run_scrapers.py --scraper representacoes_fiscais_scraper # Apenas coleta representações fiscais
  python run_scrapers.py --scraper representacoes_fiscais_process # Apenas processamento representações fiscais
  python run_scrapers.py --no-clean                              # Não limpa as tabelas antes
  python run_scrapers.py --clean-files                           # Apenas limpa arquivos antigos
        """
    )
    
    parser.add_argument(
        '--scraper',
        choices=['private', 'public', 'maritimos', 'fronteira', 'suframa', 'portos', 'representacoes_fiscais_scraper', 'representacoes_fiscais_process'],
        help='Executa apenas um scraper específico'
    )
    
    parser.add_argument(
        '--no-clean',
        action='store_true',
        help='Não limpa as tabelas antes da execução'
    )
    
    parser.add_argument(
        '--clean-files',
        action='store_true',
        help='Limpa apenas os arquivos antigos sem executar scrapers'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Saída mais detalhada'
    )
    
    args = parser.parse_args()
    
    # Criar instância do gerenciador
    manager = BrasilDataHubScrapersManager()
    
    try:
        if args.clean_files:
            # Executar apenas limpeza de arquivos
            print("🧹 Executando limpeza de arquivos antigos...")
            cleanup_all_data_files()
            print("✅ Limpeza concluída!")
            sys.exit(0)
        elif args.scraper:
            # Executar apenas um scraper
            # Note: A limpeza agora é feita pelo próprio scraper após validar os dados
            result = manager.run_single_scraper(args.scraper)
            
            # Status de saída baseado no sucesso
            sys.exit(0 if result['success'] else 1)
        else:
            # Executar todos os scrapers
            summary = manager.run_all_scrapers(clean_tables=not args.no_clean)
            
            # Status de saída baseado no sucesso geral
            if summary['successful_scrapers'] == summary['total_scrapers']:
                sys.exit(0)  # Sucesso total
            elif summary['successful_scrapers'] > 0:
                sys.exit(2)  # Sucesso parcial
            else:
                sys.exit(1)  # Falha total
                
    except KeyboardInterrupt:
        print("\n🛑 Execução interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
