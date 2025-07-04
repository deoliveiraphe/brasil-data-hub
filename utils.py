"""
Utilitários para limpeza e manutenção de arquivos de dados.
"""

import os
import glob
from pathlib import Path
from typing import List


def clean_old_files(directory: str, pattern: str, keep_count: int) -> int:
    """
    Remove arquivos antigos mantendo apenas os mais recentes.
    
    Args:
        directory (str): Diretório onde buscar os arquivos
        pattern (str): Padrão de nome dos arquivos (ex: 'aerodromos_privados_*.json')
        keep_count (int): Quantidade de arquivos mais recentes para manter
        
    Returns:
        int: Número de arquivos removidos
    """
    files_pattern = os.path.join(directory, pattern)
    files = glob.glob(files_pattern)
    
    if len(files) <= keep_count:
        return 0
    
    # Ordenar por data de modificação (mais recentes primeiro)
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Arquivos para remover (todos exceto os mais recentes)
    files_to_remove = files[keep_count:]
    
    removed_count = 0
    for file_path in files_to_remove:
        try:
            os.remove(file_path)
            removed_count += 1
            print(f"   🗑️ Removido: {Path(file_path).name}")
        except Exception as e:
            print(f"   ⚠️ Erro ao remover {file_path}: {e}")
    
    return removed_count


def cleanup_data_files(scraper_name: str) -> None:
    """
    Limpa arquivos antigos de um scraper específico.
    
    Mantém:
    - 1 arquivo raw mais recente
    - 2 arquivos processed mais recentes
    
    Args:
        scraper_name (str): Nome base do scraper (ex: 'aerodromos_privados')
    """
    print(f"🧹 Limpando arquivos antigos de {scraper_name}...")
    
    # Limpar arquivos raw (manter apenas 1)
    raw_removed = clean_old_files(
        directory='data/raw',
        pattern=f'{scraper_name}_raw_*.json',
        keep_count=1
    )
    
    # Limpar arquivos processed (manter apenas 2)
    processed_removed = clean_old_files(
        directory='data/processed',
        pattern=f'{scraper_name}_*.json',
        keep_count=2
    )
    
    total_removed = raw_removed + processed_removed
    
    if total_removed > 0:
        print(f"✅ Limpeza concluída: {total_removed} arquivos removidos")
        print(f"   📄 Raw: {raw_removed} removidos (mantendo 1)")
        print(f"   📋 Processed: {processed_removed} removidos (mantendo 2)")
    else:
        print("✅ Nenhum arquivo antigo encontrado para remoção")


def cleanup_all_data_files() -> None:
    """
    Limpa arquivos antigos de todos os scrapers conhecidos.
    """
    print("🧹 Iniciando limpeza geral de arquivos antigos...")
    
    scrapers = [
        'aerodromos_privados',
        'aerodromos_publicos'
    ]
    
    total_cleaned = 0
    
    for scraper in scrapers:
        print(f"\n{'='*50}")
        cleanup_data_files(scraper)
        total_cleaned += 1
    
    print(f"\n✅ Limpeza geral concluída para {total_cleaned} scrapers")


if __name__ == '__main__':
    # Executar limpeza geral se chamado diretamente
    cleanup_all_data_files()
