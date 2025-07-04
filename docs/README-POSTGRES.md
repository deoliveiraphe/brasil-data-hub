# 🐘 Guia de Configuração PostgreSQL com Docker - TheTrace

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- DBeaver (ou outro cliente PostgreSQL)

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# 1. Ajuste as configurações no arquivo .env (já criado)
# Edite o arquivo .env com suas credenciais desejadas

# 2. Inicie o ambiente PostgreSQL
./manage-db.sh start
```

### 2. Comandos Disponíveis

```bash
./manage-db.sh start     # Inicia PostgreSQL e PgAdmin
./manage-db.sh stop      # Para os serviços
./manage-db.sh restart   # Reinicia os serviços
./manage-db.sh status    # Mostra informações de conexão
./manage-db.sh logs      # Mostra logs em tempo real
./manage-db.sh backup    # Cria backup do banco
./manage-db.sh connect   # Conecta via psql no terminal
./manage-db.sh clean     # Remove todos os dados (CUIDADO!)
./manage-db.sh help      # Ajuda completa
```

## 🔌 Configuração no DBeaver

### Método 1: Conexão Direta

1. **Abra o DBeaver**
2. **Clique em "Nova Conexão"**
3. **Selecione PostgreSQL**
4. **Configure os dados de conexão:**

   ```
   Host: localhost
   Porta: 5432
   Database: thetrace_db
   Usuário: thetrace_user
   Senha: MinhaSenh@Segura123!
   ```

5. **Teste a conexão** clicando em "Test Connection"
6. **Clique em "Finish"**

### Método 2: Via URL de Conexão

1. **No DBeaver, vá em "Database" → "New Database Connection"**
2. **Selecione PostgreSQL**
3. **Na aba "Main", clique em "URL"**
4. **Cole a URL de conexão:**
   ```
   postgresql://thetrace_user:MinhaSenh@Segura123!@localhost:5432/thetrace_db
   ```

## 🌐 Interface Web (PgAdmin)

Além do DBeaver, você também pode usar o PgAdmin via navegador:

- **URL:** http://localhost:8080
- **Email:** admin@thetrace.com
- **Senha:** admin123

### Configurando Servidor no PgAdmin:

1. Acesse http://localhost:8080
2. Faça login com as credenciais acima
3. Clique em "Add New Server"
4. **Na aba "General":** Nome = "TheTrace Local"
5. **Na aba "Connection":**
   - Host: postgres (nome do container)
   - Port: 5432
   - Database: thetrace_db
   - Username: thetrace_user
   - Password: MinhaSenh@Segura123!

## 📁 Estrutura de Arquivos Criada

```
thetrace/
├── docker-compose.yml          # Configuração dos containers
├── .env                        # Variáveis de ambiente (suas credenciais)
├── .env.example               # Exemplo de configuração
├── manage-db.sh               # Script de gerenciamento
├── docker/
│   └── postgres/
│       └── init/
│           └── 01-init.sql    # Script de inicialização do banco
└── backups/                   # Pasta para backups (criada automaticamente)
```

## 🔒 Segurança

### ⚠️ IMPORTANTE - Altere as Senhas!

As senhas padrão são apenas para desenvolvimento. **SEMPRE** altere em produção:

1. Edite o arquivo `.env`
2. Use senhas fortes com caracteres especiais
3. Nunca commite o arquivo `.env` no git

### 🛡️ Boas Práticas Implementadas

- ✅ Uso de variáveis de ambiente para credenciais
- ✅ Healthcheck para verificar se o PostgreSQL está pronto
- ✅ Volumes persistentes para dados
- ✅ Rede isolada para os containers
- ✅ Restart automático dos containers
- ✅ Scripts de inicialização seguros

## 🔧 Troubleshooting

### Problema: "Porta 5432 já está em uso"

```bash
# Verifique se há outro PostgreSQL rodando
sudo ss -tlnp | grep 5432

# Se houver, pare o serviço local do PostgreSQL
sudo systemctl stop postgresql
```

### Problema: "Permissão negada no script"

```bash
# Torne o script executável
chmod +x manage-db.sh
```

### Problema: "Docker não está rodando"

```bash
# Inicie o Docker
sudo systemctl start docker
# ou no macOS/Windows: inicie o Docker Desktop
```

## 📊 Recursos Incluídos

### Extensões PostgreSQL Ativadas:

- **uuid-ossp:** Para geração de UUIDs
- **pgcrypto:** Para funções criptográficas

### Schema Exemplo:

- Schema `thetrace` com tabela `usuarios` de exemplo
- Índices otimizados para performance
- Campos com tipos apropriados e constraints

## 🚀 Próximos Passos

1. **Configure sua aplicação Python** para usar a string de conexão do `.env`
2. **Crie suas tabelas** adicionando scripts em `docker/postgres/init/`
3. **Configure backups automáticos** usando cron jobs
4. **Use migrações** com Alembic (SQLAlchemy) ou Django migrations

## 📝 Exemplo de Uso em Python

```python
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Conecta ao banco usando a URL do .env
engine = create_engine(os.getenv('DATABASE_URL'))
```

---

**🎉 Pronto! Seu ambiente PostgreSQL está configurado e seguro!**
