# 🐍 Guia do Ambiente Virtual Python - TheTrace

## 📋 Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Configuração Inicial

### 1. Ambiente Virtual

O ambiente virtual já foi criado em `.venv`. Para gerenciá-lo:

```bash
# Mostra informações do ambiente
./manage-python.sh info

# Instala dependências de desenvolvimento
./manage-python.sh install-dev

# Instala apenas dependências de produção
./manage-python.sh install
```

### 2. Ativação Manual do Ambiente

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Desativar ambiente virtual
deactivate
```

## 🛠️ Comandos Disponíveis

### Script de Gerenciamento

```bash
./manage-python.sh create      # Cria o ambiente virtual
./manage-python.sh install     # Instala dependências de produção
./manage-python.sh install-dev # Instala dependências de desenvolvimento
./manage-python.sh info        # Mostra informações do ambiente
./manage-python.sh run         # Executa a aplicação
./manage-python.sh format      # Formata o código (black + isort)
./manage-python.sh lint        # Verifica qualidade do código
./manage-python.sh clean       # Limpa cache Python
./manage-python.sh backup      # Cria backup dos requirements
./manage-python.sh help        # Mostra ajuda completa
```

## 🏃‍♂️ Executando a Aplicação

### Método 1: Via Script de Gerenciamento

```bash
./manage-python.sh run
```

### Método 2: Manual

```bash
# Ative o ambiente virtual primeiro
source .venv/bin/activate

# Execute a aplicação
python -m uvicorn src.thetrace.main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em:

- **API:** http://localhost:8000
- **Documentação:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 📦 Estrutura de Dependências

### Arquivos de Requirements

- **`requirements-prod.txt`** - Dependências mínimas para produção
- **`requirements-dev.txt`** - Dependências de desenvolvimento (inclui produção)
- **`requirements.txt`** - Todas as dependências (legacy)
- **`pyproject.toml`** - Configuração Poetry e ferramentas

### Principais Bibliotecas

#### Produção:

- **FastAPI** - Framework web moderno e rápido
- **Uvicorn** - Servidor ASGI para FastAPI
- **SQLAlchemy** - ORM para banco de dados
- **Alembic** - Migrações de banco de dados
- **psycopg2-binary** - Driver PostgreSQL
- **Pydantic** - Validação de dados
- **python-dotenv** - Carregamento de variáveis de ambiente

#### Desenvolvimento:

- **Black** - Formatador de código
- **isort** - Organizador de imports
- **Flake8** - Linter de código
- **MyPy** - Verificador de tipos
- **Bandit** - Verificador de segurança

## 🎨 Qualidade de Código

### Formatação Automática

```bash
# Formatar código
./manage-python.sh format
```

### Verificação de Qualidade

```bash
# Verificar qualidade do código
./manage-python.sh lint
```

### Limpeza de Cache

```bash
# Limpar arquivos temporários
./manage-python.sh clean
```

## 📁 Estrutura do Projeto

```
thetrace/
├── src/
│   └── thetrace/
│       ├── __init__.py
│       ├── main.py           # Aplicação FastAPI principal
│       └── config.py         # Configurações da aplicação
├── .venv/                    # Ambiente virtual Python
├── docker-compose.yml        # PostgreSQL com Docker
├── .env                      # Variáveis de ambiente
├── requirements-prod.txt     # Dependências de produção
├── requirements-dev.txt      # Dependências de desenvolvimento
├── pyproject.toml           # Configuração Poetry e ferramentas
├── manage-python.sh         # Script de gerenciamento Python
└── manage-db.sh            # Script de gerenciamento do banco
```

## 🔧 Configuração

### Variáveis de Ambiente

As configurações são gerenciadas pelo arquivo `.env`:

```bash
# Configurações da aplicação
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# Configurações do banco (já definidas para PostgreSQL local)
DATABASE_URL=postgresql://thetrace_user:MinhaSenh@Segura123!@localhost:5432/thetrace_db
```

### Configurações do Poetry

O arquivo `pyproject.toml` contém todas as configurações das ferramentas:

- **Black:** Formatação de código (linha máxima 88 caracteres)
- **isort:** Organização de imports compatível com Black
- **MyPy:** Verificação de tipos rigorosa
- **Flake8:** Linting básico

## 🚀 Próximos Passos

1. **Inicie o banco PostgreSQL:**

   ```bash
   ./manage-db.sh start
   ```

2. **Configure o ambiente Python:**

   ```bash
   ./manage-python.sh install-dev
   ```

3. **Execute a aplicação:**

   ```bash
   ./manage-python.sh run
   ```

4. **Acesse a documentação:** http://localhost:8000/docs

## 💡 Dicas de Desenvolvimento

- Use `./manage-python.sh format` antes de cada commit
- Execute `./manage-python.sh lint` para verificar a qualidade
- Mantenha o ambiente virtual sempre ativado durante o desenvolvimento
- Use type hints em todas as funções (configurado no MyPy)
- Siga o padrão PEP 8 (Black cuida disso automaticamente)

---

**🎉 Ambiente Python configurado e pronto para desenvolvimento!**
