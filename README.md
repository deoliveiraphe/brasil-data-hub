# 🇧🇷 Brasil Data Hub

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)
[![Web Scraping](https://img.shields.io/badge/Web-Scraping-green.svg)](https://github.com)
[![Data Engineering](https://img.shields.io/badge/Data-Engineering-orange.svg)](https://github.com)

> **Sistema modular de coleta e processamento de dados governamentais brasileiros através de web scraping automatizado**

## 🎯 Sobre o Projeto

O **Brasil Data Hub** é um sistema completo de **engenharia de dados** que demonstra habilidades avançadas em:

- **Web Scraping** de fontes governamentais complexas
- **Processamento de dados** em larga escala
- **Arquitetura modular** e escalável
- **Gerenciamento de banco de dados** com PostgreSQL
- **Containerização** com Docker
- **Automação** de processos ETL

O projeto coleta dados de múltiplas fontes oficiais brasileiras e os centraliza em um banco estruturado para análises e consultas.

## 🛠️ Stack Tecnológico

### **Backend & Scraping**
- **Python 3.8+** - Linguagem principal
- **SQLAlchemy** - ORM para banco de dados
- **Selenium** - Automação de navegador
- **BeautifulSoup** - Parsing HTML
- **Requests** - Cliente HTTP
- **Pandas** - Manipulação de dados

### **Banco de Dados**
- **PostgreSQL 15** - Banco principal
- **Alembic** - Migrações de schema
- **PgAdmin** - Interface de administração

### **DevOps & Infraestrutura**
- **Docker Compose** - Orquestração de containers
- **Shell Scripts** - Automação de tarefas
- **Logging** - Monitoramento de execução

## 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Sources   │    │   Scrapers      │    │   Database      │
│                 │    │                 │    │                 │
│ • ANAC          │───▶│ • Modular       │───▶│ • PostgreSQL    │
│ • Receita Fed.  │    │ • Concurrent    │    │ • Structured    │
│ • IBGE          │    │ • Resilient     │    │ • Indexed       │
│ • ANTAQ         │    │ • Logging       │    │ • Backup        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Padrões de Design Implementados**
- **Factory Pattern** - Criação de scrapers
- **Strategy Pattern** - Diferentes abordagens de scraping
- **Observer Pattern** - Logging e monitoramento
- **Singleton Pattern** - Conexão com banco de dados

## 📊 Fontes de Dados Coletadas

### ✈️ **Aviação Civil (ANAC)**
- **Aeródromos Privados**: 3.600+ com geolocalização
- **Aeródromos Públicos**: 500+ com dados operacionais

### 🏛️ **Receita Federal**
- **Representações Fiscais**: Unidades da RFB em todo Brasil

### 🌊 **Dados Geográficos (IBGE)**
- **Municípios Marítimos**: 395 cidades costeiras
- **Municípios de Fronteira**: 588 cidades limítrofes
- **Zonas Especiais SUFRAMA**: 94 municípios

### 🚢 **Transporte Aquaviário (ANTAQ)**
- **Atracações Portuárias**: Infraestrutura nacional

## 🚀 Início Rápido

### **1. Configuração do Ambiente**

```bash
# Clonar o repositório
git clone <repository-url>
cd brasil-data-hub

# Criar ambiente virtual Python
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### **2. Iniciar Banco de Dados**

```bash
# Iniciar PostgreSQL + PgAdmin
./manage-db.sh start

# Verificar status
./manage-db.sh status
```

### **3. Executar Coleta de Dados**

```bash
# Executar todos os scrapers
python run_scrapers.py

# Executar scraper específico
python run_scrapers.py --scraper private

# Modo verboso
python run_scrapers.py --verbose
```

## 📁 Estrutura do Projeto

```
brasil-data-hub/
├── 🔧 Automação
│   └── manage-db.sh           # Gerenciamento PostgreSQL
│
├── 🐍 Aplicação Principal
│   ├── run_scrapers.py        # Orquestrador principal
│   ├── models.py              # Modelos de dados
│   ├── database.py            # Conexão e configuração
│   └── utils.py               # Utilitários
│
├── 🕷️ Scrapers Modulares
│   ├── scrapers/
│   │   ├── aerodromos_privados.py
│   │   ├── aerodromos_publicos.py
│   │   ├── representacoes_fiscais.py
│   │   ├── municipios_*.py
│   │   └── atracacoes_portuarias.py
│
├── 🗄️ Infraestrutura
│   ├── docker-compose.yml     # Orquestração Docker
│   ├── alembic/               # Migrações
│   └── requirements.txt       # Dependências
│
├── 📊 Dados e Logs
│   ├── data/                  # Dados coletados
│   ├── logs/                  # Logs de execução
│   └── backups/               # Backups automáticos
│
└── 📚 Documentação
    └── docs/                  # Documentação técnica
```

## 🔌 Gerenciamento Automatizado

### **🐘 Gerenciamento PostgreSQL**

```bash
./manage-db.sh start          # Iniciar serviços
./manage-db.sh stop           # Parar serviços
./manage-db.sh status         # Status detalhado
./manage-db.sh backup         # Backup automático
./manage-db.sh connect        # Conectar via psql
```

### **🐍 Ferramentas de Desenvolvimento**

```bash
# Formatação de código
black .
isort . --profile black

# Análise de qualidade
flake8 .
mypy . --ignore-missing-imports

# Testes
pytest
```

## 🗃️ Banco de Dados

### **Configuração de Acesso**
- **Host**: localhost:5432
- **Banco**: brasil_data_hub
- **PgAdmin**: http://localhost:8080

### **Tabelas Principais**

| Tabela | Registros | Descrição |
|--------|-----------|-----------|
| `aerodromos_privados` | 3.600+ | Aeródromos privados nacionais |
| `aerodromos_publicos` | 500+ | Aeródromos públicos e comerciais |
| `representacoes_fiscais` | 120+ | Unidades da Receita Federal |
| `municipios_maritimos` | 395 | Municípios defrontantes com o mar |
| `municipios_fronteira` | 588 | Municípios da faixa de fronteira |
| `municipios_suframa` | 94 | Zonas fiscais especiais |
| `atracacoes_portuarias` | 200+ | Infraestrutura portuária |

## 🔍 Principais Funcionalidades

### **Web Scraping Avançado**
- **Multi-source**: Coleta de diversas APIs e sites
- **Resiliente**: Retry automático e tratamento de erros
- **Eficiente**: Processamento concorrente
- **Monitorado**: Logging detalhado de execução

### **Processamento de Dados**
- **Validação**: Verificação de integridade
- **Transformação**: Normalização e limpeza
- **Geolocalização**: Processamento de coordenadas
- **Deduplicação**: Remoção de registros duplicados

### **Gerenciamento de Banco**
- **Migrações**: Versionamento de schema
- **Backup**: Backup automático
- **Indexação**: Otimização de consultas
- **Monitoramento**: Estatísticas de uso

## 📈 Exemplo de Execução

```
🚀 Iniciando coleta de dados...
📅 07/01/2025 08:44:00

🧹 Preparando ambiente...
✅ Banco de dados conectado

======================================================================
🎯 Executando: Aeródromos Privados
======================================================================
🔍 Coletando dados da ANAC...
✅ 3.603 aeródromos encontrados
💾 Salvando no banco...
✅ Dados salvos com sucesso

======================================================================
📈 RELATÓRIO FINAL
======================================================================
⏱️ Tempo total: 3.45 segundos
✅ Scrapers executados: 7/7
🗄️ Registros coletados: 5.301

🎉 EXECUÇÃO CONCLUÍDA COM SUCESSO!
```

## ⚙️ Configuração Avançada

### **Variáveis de Ambiente**

```env
# Banco de Dados
POSTGRES_DB=brasil_data_hub
POSTGRES_USER=brasil_user
POSTGRES_PASSWORD=senha_segura
DATABASE_URL=postgresql://brasil_user:senha_segura@localhost:5432/brasil_data_hub

# Administração
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

### **Execução Seletiva**

```bash
# Executar scraper específico
python run_scrapers.py --scraper private

# Executar sem limpeza
python run_scrapers.py --no-clean

# Modo verboso
python run_scrapers.py --verbose
```

## 🎯 Destaques Técnicos

### **Arquitetura Modular**
- Cada scraper é independente e reutilizável
- Fácil adição de novas fontes de dados
- Separação clara de responsabilidades

### **Tratamento de Erros**
- Retry automático em falhas de rede
- Logging detalhado para debugging
- Graceful degradation em falhas parciais

### **Performance**
- Processamento concorrente quando possível
- Uso eficiente de memória
- Otimização de consultas SQL

### **Manutenibilidade**
- Código bem documentado
- Testes automatizados
- Padrões de código consistentes

## 🚀 Casos de Uso

### **Análise de Dados**
- Estudos de infraestrutura nacional
- Análise geográfica e demográfica
- Pesquisa acadêmica e jornalística

### **Aplicações Comerciais**
- Planejamento logístico
- Análise de mercado regional
- Consultoria especializada

### **Compliance e Regulação**
- Verificação de dados oficiais
- Auditoria de informações
- Relatórios governamentais

## 🤝 Contribuindo

1. **Fork** o projeto
2. **Crie** uma branch para sua feature
3. **Implemente** seguindo os padrões
4. **Teste** com os scripts de qualidade
5. **Abra** um Pull Request

## 📞 Contato

**Desenvolvedor**: Paulo Henrique Oliveira  
**Email**: [seu-email@example.com]  
**LinkedIn**: [seu-linkedin]  
**GitHub**: [seu-github]

## 📄 Licença

Este projeto está sob a licença **MIT**. Veja o arquivo LICENSE para detalhes.

---

**🎯 Brasil Data Hub** - *Transformando dados governamentais em insights valiosos*
