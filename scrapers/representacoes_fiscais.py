import requests
import json
import time
import csv
from datetime import datetime
import os
import hashlib
import glob

# --- CONFIGURAÇÕES ---
url = "https://wabi-brazil-south-b-primary-api.analysis.windows.net/public/reports/querydata?synchronous=true"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'ActivityId': 'aa7a67e1-70b2-4cd3-b88e-dc745f6a7047',
    'Content-Type': 'application/json;charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://app.powerbi.com',
    'Referer': 'https://app.powerbi.com/',
    'RequestId': 'bc739e84-4c10-cf7d-2e3e-c2bea3f44254',
    'X-PowerBI-ResourceKey': '92112a76-e4f4-49c0-bcfa-68f9f89737d3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'
}

def gerar_hash_linha(linha):
    """Gera hash único para uma linha de dados"""
    linha_str = json.dumps(linha, sort_keys=True)
    return hashlib.md5(linha_str.encode()).hexdigest()

def criar_payload_com_filtro_valor(valor_minimo=None, valor_maximo=None):
    """Cria payload com filtro por valor para tentar paginação por faixas"""
    payload = {
        "version": "1.0.0",
        "queries": [{
            "Query": {
                "Commands": [{
                    "SemanticQueryDataShapeCommand": {
                        "Query": {
                            "Version": 2,
                            "From": [
                                {"Name": "p", "Entity": "Processo", "Type": 0},
                                {"Name": "m", "Entity": "Medidas", "Type": 0}
                            ],
                            "Select": [
                                {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "Valor Total Processo"
                                            }
                                        },
                                        "Function": 0
                                    },
                                    "Name": "Sum(Processo.Valor Total Processo)",
                                    "NativeReferenceName": "Valor Numérico"
                                },
                                {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "Nome Contribuinte"
                                    },
                                    "Name": "Processo.Nome Contribuinte",
                                    "NativeReferenceName": "Nome"
                                },
                                {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "p"}},
                                        "Property": "Número de Inscrição com Máscara"
                                    },
                                    "Name": "Processo.Número de Inscrição com Máscara",
                                    "NativeReferenceName": "CPF/CNPJ"
                                },
                                {
                                    "Measure": {
                                        "Expression": {"SourceRef": {"Source": "m"}},
                                        "Property": "Valor Total com Máscara"
                                    },
                                    "Name": "Medidas.Valor Total com Máscara",
                                    "NativeReferenceName": "Valor1"
                                }
                            ],
                            "OrderBy": [{
                                "Direction": 2,  # Decrescente
                                "Expression": {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {"SourceRef": {"Source": "p"}},
                                                "Property": "Valor Total Processo"
                                            }
                                        },
                                        "Function": 0
                                    }
                                }
                            }]
                        },
                        "Binding": {
                            "Primary": {"Groupings": [{"Projections": [0, 1, 2, 3]}]},
                            "DataReduction": {
                                "DataVolume": 4,
                                "Primary": {
                                    "Window": {"Count": 50000}
                                }
                            },
                            "Version": 1
                        },
                        "ExecutionMetricsKind": 1
                    }
                }]
            },
            "ApplicationContext": {
                "DatasetId": "9f56287c-4777-4fba-969b-dc3b9f07b81f",
                "Sources": [{
                    "ReportId": "ec1978a7-010a-4aca-8337-95c4a15a97a3",
                    "VisualId": "7bfaa991cf7efd64fa0d"
                }]
            }
        }],
        "cancelQueries": [],
        "modelId": 6107597
    }
    
    # Adiciona filtro por valor se especificado
    if valor_minimo is not None or valor_maximo is not None:
        filtro = {
            "Filter": {
                "Version": 2,
                "From": [{"Name": "p", "Entity": "Processo", "Type": 0}],
                "Where": []
            }
        }
        
        if valor_minimo is not None:
            filtro["Filter"]["Where"].append({
                "Condition": {
                    "Comparison": {
                        "ComparisonKind": 2,  # Greater than or equal
                        "Left": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "p"}},
                                "Property": "Valor Total Processo"
                            }
                        },
                        "Right": {
                            "Literal": {"Value": f"'{valor_minimo}D'"}
                        }
                    }
                }
            })
        
        if valor_maximo is not None:
            filtro["Filter"]["Where"].append({
                "Condition": {
                    "Comparison": {
                        "ComparisonKind": 1,  # Less than or equal
                        "Left": {
                            "Column": {
                                "Expression": {"SourceRef": {"Source": "p"}},
                                "Property": "Valor Total Processo"
                            }
                        },
                        "Right": {
                            "Literal": {"Value": f"'{valor_maximo}D'"}
                        }
                    }
                }
            })
        
        payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"]["Query"]["Where"] = filtro["Filter"]["Where"]
    
    return payload

def criar_payload_ordenacao_crescente():
    """Cria payload com ordenação crescente para tentar pegar registros do "final"."""
    payload = criar_payload_com_filtro_valor()
    # Muda direção da ordenação para crescente
    payload["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"]["Query"]["OrderBy"][0]["Direction"] = 1
    return payload

def extrair_com_diferentes_ordenacoes():
    """Tenta extrair dados com diferentes ordenações para pegar registros diferentes"""
    print("🔄 Tentando diferentes ordenações...")
    
    todos_dados = {}  # Usar hash como chave para evitar duplicatas
    
    # 1. Ordenação decrescente (padrão)
    print("\n📊 Extraindo com ordenação DECRESCENTE (valores altos primeiro)...")
    payload_desc = criar_payload_com_filtro_valor()
    
    try:
        response = requests.post(url, headers=headers, json=payload_desc, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        
        data = response_data['results'][0]['result']['data']
        headers_info = [item['Name'] for item in data['descriptor']['Select']]
        rows = data['dsr']['DS'][0]['PH'][0]['DM0']
        
        for row in rows:
            if 'C' in row:
                values = row['C']
                linha = {
                    headers_info[0]: values[0] if len(values) > 0 else None,
                    headers_info[1]: values[1] if len(values) > 1 else None,
                    headers_info[2]: values[2] if len(values) > 2 else None,
                    headers_info[3]: values[3] if len(values) > 3 else None,
                }
                hash_linha = gerar_hash_linha(linha)
                todos_dados[hash_linha] = linha
        
        print(f"✅ Decrescente: {len(rows):,} registros coletados")
        
    except Exception as e:
        print(f"❌ Erro na ordenação decrescente: {e}")
    
    # 2. Ordenação crescente
    print("\n📊 Extraindo com ordenação CRESCENTE (valores baixos primeiro)...")
    payload_asc = criar_payload_ordenacao_crescente()
    
    try:
        response = requests.post(url, headers=headers, json=payload_asc, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        
        data = response_data['results'][0]['result']['data']
        rows = data['dsr']['DS'][0]['PH'][0]['DM0']
        
        novos_registros = 0
        for row in rows:
            if 'C' in row:
                values = row['C']
                linha = {
                    headers_info[0]: values[0] if len(values) > 0 else None,
                    headers_info[1]: values[1] if len(values) > 1 else None,
                    headers_info[2]: values[2] if len(values) > 2 else None,
                    headers_info[3]: values[3] if len(values) > 3 else None,
                }
                hash_linha = gerar_hash_linha(linha)
                if hash_linha not in todos_dados:
                    todos_dados[hash_linha] = linha
                    novos_registros += 1
        
        print(f"✅ Crescente: {len(rows):,} registros coletados ({novos_registros:,} novos)")
        
    except Exception as e:
        print(f"❌ Erro na ordenação crescente: {e}")
    
    # 3. Sem ordenação (remover OrderBy)
    print("\n📊 Extraindo SEM ORDENAÇÃO...")
    payload_sem_ordem = criar_payload_com_filtro_valor()
    del payload_sem_ordem["queries"][0]["Query"]["Commands"][0]["SemanticQueryDataShapeCommand"]["Query"]["OrderBy"]
    
    try:
        response = requests.post(url, headers=headers, json=payload_sem_ordem, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        
        data = response_data['results'][0]['result']['data']
        rows = data['dsr']['DS'][0]['PH'][0]['DM0']
        
        novos_registros = 0
        for row in rows:
            if 'C' in row:
                values = row['C']
                linha = {
                    headers_info[0]: values[0] if len(values) > 0 else None,
                    headers_info[1]: values[1] if len(values) > 1 else None,
                    headers_info[2]: values[2] if len(values) > 2 else None,
                    headers_info[3]: values[3] if len(values) > 3 else None,
                }
                hash_linha = gerar_hash_linha(linha)
                if hash_linha not in todos_dados:
                    todos_dados[hash_linha] = linha
                    novos_registros += 1
        
        print(f"✅ Sem ordenação: {len(rows):,} registros coletados ({novos_registros:,} novos)")
        
    except Exception as e:
        print(f"❌ Erro sem ordenação: {e}")
    
    print(f"\n🎯 TOTAL ÚNICO: {len(todos_dados):,} registros únicos coletados")
    return list(todos_dados.values()), headers_info

def tentar_multiplas_requisicoes_com_delay():
    """Tenta fazer múltiplas requisições com delay, na esperança de pegar dados diferentes"""
    print("\n🔄 Tentando múltiplas requisições com delay...")
    
    todos_dados = {}
    payload_base = criar_payload_com_filtro_valor()
    
    for i in range(5):  # 5 tentativas
        print(f"\n📊 Requisição {i+1}/5...")
        
        try:
            response = requests.post(url, headers=headers, json=payload_base, timeout=60)
            response.raise_for_status()
            response_data = response.json()
            
            data = response_data['results'][0]['result']['data']
            headers_info = [item['Name'] for item in data['descriptor']['Select']]
            rows = data['dsr']['DS'][0]['PH'][0]['DM0']
            
            novos_registros = 0
            for row in rows:
                if 'C' in row:
                    values = row['C']
                    linha = {
                        headers_info[0]: values[0] if len(values) > 0 else None,
                        headers_info[1]: values[1] if len(values) > 1 else None,
                        headers_info[2]: values[2] if len(values) > 2 else None,
                        headers_info[3]: values[3] if len(values) > 3 else None,
                    }
                    hash_linha = gerar_hash_linha(linha)
                    if hash_linha not in todos_dados:
                        todos_dados[hash_linha] = linha
                        novos_registros += 1
            
            print(f"✅ Requisição {i+1}: {len(rows):,} registros ({novos_registros:,} novos)")
            
            if novos_registros == 0 and i > 0:
                print("⚠️  Nenhum registro novo. Parando tentativas.")
                break
                
            time.sleep(10)  # Espera 10 segundos entre requisições
            
        except Exception as e:
            print(f"❌ Erro na requisição {i+1}: {e}")
    
    print(f"\n🎯 TOTAL ÚNICO: {len(todos_dados):,} registros únicos coletados")
    return list(todos_dados.values()), headers_info

def executar_estrategias_avancadas():
    """Executa todas as estratégias para maximizar a extração de dados"""
    print("🚀 ESTRATÉGIAS AVANÇADAS PARA CONTORNAR LIMITE DE 30K")
    print("="*60)
    
    # Estratégia 1: Diferentes ordenações
    dados_ordenacao, headers_info = extrair_com_diferentes_ordenacoes()
    
    # Estratégia 2: Múltiplas requisições
    dados_multiplas, _ = tentar_multiplas_requisicoes_com_delay()
    
    # Combina todos os dados únicos
    todos_dados_unicos = {}
    
    # Adiciona dados da estratégia de ordenação
    for linha in dados_ordenacao:
        hash_linha = gerar_hash_linha(linha)
        todos_dados_unicos[hash_linha] = linha
    
    # Adiciona dados das múltiplas requisições
    for linha in dados_multiplas:
        hash_linha = gerar_hash_linha(linha)
        todos_dados_unicos[hash_linha] = linha
    
    dados_finais = list(todos_dados_unicos.values())
    
    print(f"\n🎯 RESULTADO FINAL: {len(dados_finais):,} registros únicos")
    
    # Salva resultado final
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f'data/processed/representacoes_fiscais_{timestamp}.csv'
    os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers_info)
        writer.writeheader()
        writer.writerows(dados_finais)
    
    print(f"💾 Arquivo salvo: {nome_arquivo}")
    print(f"📊 TOTAL FINAL: {len(dados_finais):,} registros únicos")
    
    # Limpa arquivos antigos, mantendo apenas os 2 mais recentes
    limpar_arquivos_antigos()
    
    # Análise de limitação
    if len(dados_finais) == 30000:
        print("\n⚠️  LIMITAÇÃO CONFIRMADA:")
        print("   A API PowerBI tem um limite hard-coded de 30.000 registros")
        print("   Independente da estratégia usada, não é possível extrair mais dados")
        print("   via API pública.")
    elif len(dados_finais) > 30000:
        print(f"\n🎉 SUCESSO PARCIAL:")
        print(f"   Conseguimos extrair {len(dados_finais):,} registros únicos!")
        print("   Isso representa uma melhoria em relação ao limite padrão.")
    
    return nome_arquivo

def limpar_arquivos_antigos(diretorio="data/processed", padrao="representacoes_fiscais_*.csv", manter=2):
    """
    Remove arquivos antigos, mantendo apenas os mais recentes
    
    Args:
        diretorio: Diretório onde estão os arquivos
        padrao: Padrão dos arquivos a serem gerenciados
        manter: Número de arquivos mais recentes para manter
    """
    try:
        # Cria o caminho completo do padrão
        caminho_padrao = os.path.join(diretorio, padrao)
        
        # Lista todos os arquivos que correspondem ao padrão
        arquivos = glob.glob(caminho_padrao)
        
        if len(arquivos) <= manter:
            return  # Não há arquivos suficientes para remover
        
        # Ordena os arquivos por data de modificação (mais recente primeiro)
        arquivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Remove os arquivos mais antigos
        arquivos_para_remover = arquivos[manter:]
        
        for arquivo in arquivos_para_remover:
            try:
                os.remove(arquivo)
                nome_arquivo = os.path.basename(arquivo)
                print(f"🗑️  Arquivo antigo removido: {nome_arquivo}")
            except Exception as e:
                print(f"❌ Erro ao remover {arquivo}: {e}")
                
    except Exception as e:
        print(f"❌ Erro na limpeza de arquivos: {e}")

if __name__ == "__main__":
    executar_estrategias_avancadas()
    limpar_arquivos_antigos()
