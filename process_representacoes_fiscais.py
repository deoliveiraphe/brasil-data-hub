"""
Script para processar CSV de representações fiscais e inserir no PostgreSQL.
"""

import pandas as pd
import re
import os
import time
import logging
from datetime import datetime
from decimal import InvalidOperation
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database import engine, create_tables, SessionLocal
from models import RepresentacaoFiscal

# --- CONFIGURAÇÕES ---
BATCH_SIZE = 1000   # Registros por inserção no banco

# --- CONFIGURAÇÃO DE LOGS ---
def configurar_logs():
    """Configura sistema de logs para arquivo e console."""
    os.makedirs('logs', exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f'logs/process_representacoes_{timestamp}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(__name__)
    logger.info(f"📋 Log iniciado: {log_filename}")
    logger.log_filename = log_filename
    return logger

def filtrar_dados_validos(df):
    """Não faz nenhuma validação, retorna o DataFrame como está."""
    return df

def processar_dados(df):
    """
    Processa um DataFrame de dados e retorna lista de dicionários prontos para inserção.
    MAPEAMENTO CORRETO baseado na análise dos dados reais:
    - Sum(Processo.Valor Total Processo) → NOME (EDINEI RODRIGUES DE OLIVEIRA)
    - Processo.Nome Contribuinte → CPF/CNPJ (***046789**)
    - Processo.Número de Inscrição com Máscara → VALOR NUMÉRICO (2318845.5799999996)
    - Medidas.Valor Total com Máscara → VALOR FORMATADO (R$ 2.318.845,58)
    """
    dados_processados = []
    for _, row in df.iterrows():
        cpf_cnpj = str(row.get('Processo.Nome Contribuinte', ''))
        
        # Determinar tipo de documento baseado no tamanho e filtrar apenas CPF/CNPJ válidos
        tipo_documento = None
        if len(cpf_cnpj) == 11:
            tipo_documento = 'CPF'
        elif len(cpf_cnpj) == 14:
            tipo_documento = 'CNPJ'
        else:
            # Pular registros que não sejam CPF (11) ou CNPJ (14)
            continue
        
        dados_processados.append({
            'cpf_cnpj': cpf_cnpj,  # CPF/CNPJ está aqui
            'nome': str(row.get('Sum(Processo.Valor Total Processo)', '')),  # Nome está aqui
            'valor_numerico': row.get('Processo.Número de Inscrição com Máscara', None),  # Valor numérico está aqui
            'valor_formatado': str(row.get('Medidas.Valor Total com Máscara', '')),  # Valor formatado está correto
            'tipo_documento': tipo_documento,
            'mascarado': None,
            'scraped_at': datetime.now()
        })
    return dados_processados

def inserir_batch_otimizado(session, dados_batch):
    """Insere um batch de dados usando bulk insert otimizado."""
    if not dados_batch:
        return 0
    
    try:
        session.bulk_insert_mappings(RepresentacaoFiscal, dados_batch)
        session.commit()
        return len(dados_batch)
    except Exception as e:
        session.rollback()
        print(f"⚠️  Erro ao inserir batch: {e}")
        inserted = 0
        for item in dados_batch:
            try:
                obj = RepresentacaoFiscal(**item)
                session.add(obj)
                session.commit()
                inserted += 1
            except Exception as individual_error:
                session.rollback()
                print(f"⚠️  Registro problemático ignorado: {individual_error}")
        return inserted

def otimizar_banco_para_insercao(session):
    """Otimiza o banco para inserções em massa."""
    print("⚙️  Otimizando banco para inserções em massa...")
    try:
        session.execute(text("ALTER TABLE representacoes_fiscais SET (autovacuum_enabled = false);"))
        session.execute(text("SET work_mem = '256MB';"))
        session.execute(text("SET synchronous_commit = off;"))
        session.commit()
        print("✅ Otimizações aplicadas")
    except Exception as e:
        print(f"⚠️  Erro ao aplicar otimizações: {e}")
        session.rollback()

def restaurar_otimizacoes_banco(session):
    """Restaura configurações padrão do banco após inserção."""
    print("🔧 Restaurando configurações padrão do banco...")
    try:
        session.execute(text("ALTER TABLE representacoes_fiscais SET (autovacuum_enabled = true);"))
        session.execute(text("RESET work_mem;"))
        session.execute(text("RESET synchronous_commit;"))
        session.commit()
        session.close()
        with engine.connect() as conn:
            conn.execution_options(isolation_level="AUTOCOMMIT")
            conn.execute(text("VACUUM ANALYZE representacoes_fiscais;"))
        print("✅ Configurações restauradas e tabela otimizada")
    except Exception as e:
        print(f"⚠️  Erro ao restaurar configurações: {e}")

def testar_conexao_banco():
    """Testa a conexão com o banco de dados."""
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(text("SELECT 1"))
        session.close()
        return True, None
    except Exception as e:
        return False, str(e)

def mostrar_estatisticas_banco(session):
    """Mostra estatísticas da tabela após inserção."""
    print("\n📊 Estatísticas finais do banco:")
    try:
        total = session.query(RepresentacaoFiscal).count()
        print(f"   Total de registros: {total:,}")
        
        cpf_count = session.query(RepresentacaoFiscal).filter(RepresentacaoFiscal.tipo_documento == 'CPF').count()
        cnpj_count = session.query(RepresentacaoFiscal).filter(RepresentacaoFiscal.tipo_documento == 'CNPJ').count()
        mascarados = session.query(RepresentacaoFiscal).filter(RepresentacaoFiscal.mascarado == 'SIM').count()
        valor_total = session.execute(text("SELECT SUM(valor_numerico) FROM representacoes_fiscais WHERE valor_numerico IS NOT NULL")).scalar() or 0
        
        print(f"   CPF: {cpf_count:,}")
        print(f"   CNPJ: {cnpj_count:,}")
        print(f"   Documentos mascarados: {mascarados:,}")
        print(f"   Valor total: R$ {valor_total:,.2f}")
    except Exception as e:
        print(f"⚠️  Erro ao buscar estatísticas: {e}")

def processar_csv(caminho_arquivo, logger=None):
    """Processa o arquivo CSV de uma só vez."""
    print(f"🎯 Iniciando processamento do arquivo: {caminho_arquivo}")
    if logger:
        logger.info(f"🎯 Iniciando processamento: {caminho_arquivo}")

    if not os.path.exists(caminho_arquivo):
        error_msg = f"❌ Arquivo não encontrado: {caminho_arquivo}"
        print(error_msg)
        if logger:
            logger.error(error_msg)
        return False

    file_size = os.path.getsize(caminho_arquivo)
    print(f"📏 Tamanho do arquivo: {file_size / (1024**2):.2f} MB")
    if logger:
        logger.info(f"📏 Arquivo: {file_size / (1024**2):.2f} MB ({file_size:,} bytes)")

    print("🔗 Testando conexão com PostgreSQL...")
    if logger:
        logger.info("🔗 Testando conexão com PostgreSQL...")
    
    conexao_ok, msg_erro = testar_conexao_banco()
    if not conexao_ok:
        error_msg = f"❌ Erro de conexão com PostgreSQL: {msg_erro}"
        print(error_msg)
        if logger:
            logger.error(error_msg)
        return False
    
    print("✅ Conexão com PostgreSQL estabelecida")
    if logger:
        logger.info("✅ Conexão com PostgreSQL estabelecida")

    with SessionLocal() as session:
        try:
            print("🗑️  Removendo e recriando a tabela 'representacoes_fiscais'...")
            if logger:
                logger.info("🗑️ Removendo e recriando a tabela 'representacoes_fiscais'...")
            session.execute(text("DROP TABLE IF EXISTS representacoes_fiscais CASCADE;"))
            session.commit()
            create_tables()
            if logger:
                logger.info("✅ Tabela 'representacoes_fiscais' removida e recriada com sucesso")

            otimizar_banco_para_insercao(session)
            if logger:
                logger.info("⚙️ Banco otimizado para inserções em massa")

            print("📂 Lendo o arquivo CSV...")
            df = pd.read_csv(caminho_arquivo, encoding='utf-8', low_memory=False)
            
            total_original = len(df)
            print(f"📄 Total de {total_original:,} registros lidos.")
            if logger:
                logger.info(f"📄 Total de {total_original:,} registros lidos do CSV.")

            df_valid = filtrar_dados_validos(df)
            dados_processados = processar_dados(df_valid)
            
            total_validos = len(dados_processados)
            descartados = total_original - total_validos
            print(f"✅ {total_validos:,} registros válidos para inserção.")
            print(f"🗑️ {descartados:,} registros descartados.")
            if logger:
                logger.info(f"✅ {total_validos:,} registros válidos para inserção, {descartados:,} descartados.")

            if not dados_processados:
                print("⚠️  Nenhum dado válido para inserir. Encerrando.")
                if logger:
                    logger.warning("⚠️  Nenhum dado válido para inserir.")
                return False

            # Sem remoção de duplicados para inserir todos
            dados_unicos = dados_processados
            
            total_unicos = len(dados_unicos)
            print(f"✨ {total_unicos:,} registros para inserção.")
            if logger:
                logger.info(f"✨ {total_unicos:,} registros para inserção.")

            print(f"💾 Inserindo {total_unicos:,} registros em lotes de {BATCH_SIZE}...")
            
            total_inserido = 0
            for i in range(0, len(dados_unicos), BATCH_SIZE):
                batch = dados_unicos[i:i + BATCH_SIZE]
                inserido = inserir_batch_otimizado(session, batch)
                total_inserido += inserido
                print(f"   -> Lote {i//BATCH_SIZE + 1}: {inserido} registros inseridos.")

            session.commit()
            print(f"✅ Inserção concluída: {total_inserido:,} registros no total.")
            if logger:
                logger.info(f"✅ Inserção concluída: {total_inserido:,} registros no total.")

            mostrar_estatisticas_banco(session)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante o processamento: {e}")
            if logger:
                logger.error(f"❌ Erro durante o processamento: {e}", exc_info=True)
            session.rollback()
            return False
        
        finally:
            restaurar_otimizacoes_banco(session)

def limpar_csvs_antigos():
    """Mantém apenas os 2 CSVs mais recentes de representações fiscais."""
    processed_dir = "data/processed"
    if not os.path.exists(processed_dir):
        return
    
    # Buscar todos os CSVs de representações fiscais
    csv_files = []
    for arquivo in os.listdir(processed_dir):
        if arquivo.endswith('.csv') and 'representacoes_fiscais' in arquivo:
            caminho_completo = os.path.join(processed_dir, arquivo)
            timestamp = os.path.getmtime(caminho_completo)
            csv_files.append((arquivo, caminho_completo, timestamp))
    
    # Ordenar por timestamp (mais recente primeiro)
    csv_files.sort(key=lambda x: x[2], reverse=True)
    
    # Manter apenas os 2 mais recentes
    if len(csv_files) > 2:
        print(f"🧹 Limpando CSVs antigos de representações fiscais...")
        for arquivo, caminho, _ in csv_files[2:]:
            try:
                os.remove(caminho)
                print(f"   �️ Removido: {arquivo}")
            except Exception as e:
                print(f"   ⚠️ Erro ao remover {arquivo}: {e}")

def encontrar_csv_mais_recente():
    """Encontra o CSV mais recente de representações fiscais."""
    processed_dir = "data/processed"
    
    if not os.path.exists(processed_dir):
        return None
    
    csv_files = []
    for arquivo in os.listdir(processed_dir):
        if arquivo.endswith('.csv') and 'representacoes_fiscais' in arquivo:
            caminho_completo = os.path.join(processed_dir, arquivo)
            timestamp = os.path.getmtime(caminho_completo)
            csv_files.append((arquivo, caminho_completo, timestamp))
    
    if not csv_files:
        return None
    
    # Ordenar por timestamp (mais recente primeiro)
    csv_files.sort(key=lambda x: x[2], reverse=True)
    return csv_files[0][1]  # Retorna o caminho do mais recente

def main():
    """Função principal."""
    print("� Processador de representações fiscais")
    print("📋 Sistema de logs integrado")
    
    logger = configurar_logs()
    logger.info("� Iniciando processador de representações fiscais")
    
    # Buscar automaticamente o CSV mais recente
    caminho_csv = encontrar_csv_mais_recente()
    
    if not caminho_csv:
        error_msg = "❌ Nenhum arquivo CSV de representações fiscais encontrado em data/processed/"
        print(error_msg)
        logger.error(error_msg)
        
        # Listar diretório para debug
        processed_dir = "data/processed"
        if os.path.exists(processed_dir):
            arquivos = os.listdir(processed_dir)
            print(f"📁 Arquivos encontrados em {processed_dir}:")
            for arquivo in arquivos:
                print(f"   - {arquivo}")
            logger.info(f"📁 Arquivos no diretório: {arquivos}")
        else:
            print(f"📁 Diretório {processed_dir} não existe!")
            logger.error(f"Diretório {processed_dir} não existe")
        return
    
    try:
        file_size = os.path.getsize(caminho_csv)
        size_mb = file_size / (1024**2)
        print(f"📊 Arquivo: {caminho_csv}")
        print(f"📏 Tamanho: {size_mb:.2f} MB")
        logger.info(f"📊 Arquivo selecionado: {caminho_csv} ({size_mb:.2f} MB)")
    except Exception as e:
        logger.error(f"Erro ao obter informações do arquivo: {e}")
    
    print("\n⚠️  ATENÇÃO: O processo irá remover e recriar a tabela 'representacoes_fiscais'.")
    print("📋 Logs serão salvos em tempo real no diretório 'logs/'")
    print("🚀 Iniciando processamento...")
    
    logger.info("🚀 Iniciando processamento")
    
    start_time = datetime.now()
    logger.info(f"🎯 INÍCIO DO PROCESSAMENTO - {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    sucesso = processar_csv(caminho_csv, logger=logger)
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    if sucesso:
        success_msg = "🎉 Processo concluído com sucesso!"
        print(f"\n{success_msg}")
        print("📊 Dados disponíveis na tabela 'representacoes_fiscais'")
        print(f"⏱️  Duração total: {duration}")
        logger.info(f"🎉 PROCESSAMENTO CONCLUÍDO COM SUCESSO")
        logger.info(f"⏱️ Duração total: {duration}")
        logger.info(f"📊 Dados inseridos na tabela 'representacoes_fiscais'")
    else:
        error_msg = "❌ Processo falhou. Verifique os logs para detalhes."
        print(f"\n{error_msg}")
        logger.error(f"❌ PROCESSAMENTO FALHOU - Duração: {duration}")
        
    logger.info(f"📋 Log salvo em: {getattr(logger, 'log_filename', 'N/A')}")

if __name__ == "__main__":
    main()
