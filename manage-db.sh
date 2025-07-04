#!/bin/bash

# 🐘 Script de Gerenciamento PostgreSQL - TheTrace
# Gerencia banco PostgreSQL com Docker e operações relacionadas

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configurações
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"
DB_CONTAINER="postgres"
PGADMIN_CONTAINER="pgadmin"
BACKUP_DIR="backups/database"

# Função para imprimir mensagens coloridas
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🐘 TheTrace - Gerenciamento PostgreSQL${NC}"
    echo -e "${CYAN}======================================${NC}"
}

# Verificar se Docker está instalado e rodando
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker não encontrado. Instale Docker e Docker Compose."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker não está rodando. Inicie o serviço Docker."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose não encontrado. Instale Docker Compose."
        exit 1
    fi
    
    print_success "Docker e Docker Compose encontrados"
}

# Verificar se arquivo .env existe
check_env() {
    if [ ! -f "$ENV_FILE" ]; then
        print_warning "Arquivo .env não encontrado. Criando arquivo padrão..."
        create_env_file
    fi
}

# Criar arquivo .env padrão
create_env_file() {
    cat > "$ENV_FILE" << 'EOF'
# Configurações da aplicação
APP_HOST=0.0.0.0
APP_PORT=8000
APP_DEBUG=false

# Configurações do PostgreSQL
POSTGRES_DB=thetrace_db
POSTGRES_USER=thetrace_user
POSTGRES_PASSWORD=MinhaSenh@Segura123!
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# URL de conexão do banco
DATABASE_URL=postgresql://thetrace_user:MinhaSenh@Segura123!@localhost:5432/thetrace_db

# Configurações do PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@thetrace.com
PGADMIN_DEFAULT_PASSWORD=admin123
PGADMIN_LISTEN_PORT=8080
EOF
    
    print_success "Arquivo .env criado com configurações padrão"
    print_warning "IMPORTANTE: Altere as senhas padrão para produção!"
}

# Verificar se docker-compose.yml existe
check_compose() {
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_warning "Arquivo docker-compose.yml não encontrado. Criando..."
        create_compose_file
    fi
}

# Criar arquivo docker-compose.yml
create_compose_file() {
    cat > "$COMPOSE_FILE" << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: thetrace_postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports:
      - "${POSTGRES_PORT}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - thetrace_network

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: thetrace_pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
      PGADMIN_LISTEN_PORT: 80
    ports:
      - "${PGADMIN_LISTEN_PORT}:80"
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - thetrace_network

volumes:
  postgres_data:
    driver: local
  pgadmin_data:
    driver: local

networks:
  thetrace_network:
    driver: bridge
EOF
    
    print_success "Arquivo docker-compose.yml criado"
}

# Criar estrutura de diretórios e scripts de inicialização
create_init_structure() {
    mkdir -p docker/postgres/init
    mkdir -p "$BACKUP_DIR"
    
    # Script de inicialização do banco
    cat > "docker/postgres/init/01-init.sql" << 'EOF'
-- Script de inicialização do banco TheTrace
-- Este script é executado automaticamente na criação do container

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Criar schema principal
CREATE SCHEMA IF NOT EXISTS thetrace;

-- Configurar search_path padrão
ALTER DATABASE thetrace_db SET search_path TO thetrace, public;

-- Criar tabela de exemplo (usuários)
CREATE TABLE IF NOT EXISTS thetrace.usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar índices
CREATE INDEX IF NOT EXISTS idx_usuarios_email ON thetrace.usuarios(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_ativo ON thetrace.usuarios(ativo);

-- Inserir usuário de exemplo
INSERT INTO thetrace.usuarios (nome, email, senha_hash) 
VALUES ('Admin TheTrace', 'admin@thetrace.com', crypt('admin123', gen_salt('bf')))
ON CONFLICT (email) DO NOTHING;

-- Comentários para documentação
COMMENT ON SCHEMA thetrace IS 'Schema principal da aplicação TheTrace';
COMMENT ON TABLE thetrace.usuarios IS 'Tabela de usuários do sistema';

-- Configurações de performance
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = on;
ALTER SYSTEM SET log_min_duration_statement = 1000;

-- Reload configuration
SELECT pg_reload_conf();
EOF
    
    print_success "Estrutura de inicialização criada"
}

# Iniciar serviços
start_services() {
    print_info "Iniciando serviços PostgreSQL e PgAdmin..."
    
    check_docker
    check_env
    check_compose
    create_init_structure
    
    # Carregar variáveis do .env
    source "$ENV_FILE"
    
    docker-compose up -d
    
    print_info "Aguardando PostgreSQL ficar pronto..."
    
    # Aguardar PostgreSQL ficar saudável
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if docker-compose ps postgres | grep -q "healthy"; then
            break
        fi
        sleep 2
        attempt=$((attempt + 1))
        echo -n "."
    done
    echo
    
    if [ $attempt -eq $max_attempts ]; then
        print_error "PostgreSQL não ficou pronto após 60 segundos"
        show_logs
        exit 1
    fi
    
    print_success "PostgreSQL iniciado com sucesso!"
    show_connection_info
}

# Parar serviços
stop_services() {
    print_info "Parando serviços..."
    
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose down
        print_success "Serviços parados"
    else
        print_warning "Arquivo docker-compose.yml não encontrado"
    fi
}

# Reiniciar serviços
restart_services() {
    print_info "Reiniciando serviços..."
    stop_services
    sleep 2
    start_services
}

# Mostrar status dos serviços
show_status() {
    print_header
    
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_warning "Docker Compose não configurado"
        return
    fi
    
    echo -e "${CYAN}📊 Status dos containers:${NC}"
    docker-compose ps
    echo
    
    # Verificar se PostgreSQL está respondendo
    if docker-compose ps postgres | grep -q "healthy"; then
        source "$ENV_FILE"
        echo -e "${GREEN}✅ PostgreSQL: Online e saudável${NC}"
        show_connection_info
    else
        echo -e "${RED}❌ PostgreSQL: Offline ou com problemas${NC}"
    fi
}

# Mostrar informações de conexão
show_connection_info() {
    if [ -f "$ENV_FILE" ]; then
        source "$ENV_FILE"
        
        echo ""
        echo -e "${CYAN}🔌 Informações de Conexão:${NC}"
        echo -e "${YELLOW}  PostgreSQL:${NC}"
        echo "    Host: ${POSTGRES_HOST}"
        echo "    Port: ${POSTGRES_PORT}"
        echo "    Database: ${POSTGRES_DB}"
        echo "    User: ${POSTGRES_USER}"
        echo "    Password: ${POSTGRES_PASSWORD}"
        echo ""
        echo -e "${YELLOW}  URL de Conexão:${NC}"
        echo "    ${DATABASE_URL}"
        echo ""
        echo -e "${YELLOW}  PgAdmin Web:${NC}"
        echo "    URL: http://localhost:${PGADMIN_LISTEN_PORT}"
        echo "    Email: ${PGADMIN_DEFAULT_EMAIL}"
        echo "    Password: ${PGADMIN_DEFAULT_PASSWORD}"
        echo ""
        echo -e "${BLUE}💡 Para conectar no DBeaver, use as informações PostgreSQL acima${NC}"
    fi
}

# Mostrar logs
show_logs() {
    print_info "Mostrando logs dos serviços..."
    
    if [ -f "$COMPOSE_FILE" ]; then
        docker-compose logs -f --tail=50
    else
        print_error "Docker Compose não configurado"
    fi
}

# Conectar via psql
connect_psql() {
    print_info "Conectando ao PostgreSQL via psql..."
    
    if [ ! -f "$ENV_FILE" ]; then
        print_error "Arquivo .env não encontrado"
        exit 1
    fi
    
    source "$ENV_FILE"
    
    # Verificar se PostgreSQL está rodando
    if ! docker-compose ps postgres | grep -q "healthy"; then
        print_error "PostgreSQL não está rodando. Execute: ./manage-db.sh start"
        exit 1
    fi
    
    print_info "Conectando como usuário: ${POSTGRES_USER}"
    print_info "Database: ${POSTGRES_DB}"
    print_warning "Para sair do psql, digite: \\q"
    
    docker-compose exec postgres psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"
}

# Criar backup do banco
create_backup() {
    print_info "Criando backup do banco de dados..."
    
    if [ ! -f "$ENV_FILE" ]; then
        print_error "Arquivo .env não encontrado"
        exit 1
    fi
    
    source "$ENV_FILE"
    
    # Verificar se PostgreSQL está rodando
    if ! docker-compose ps postgres | grep -q "healthy"; then
        print_error "PostgreSQL não está rodando. Execute: ./manage-db.sh start"
        exit 1
    fi
    
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    local backup_file="${BACKUP_DIR}/backup_${POSTGRES_DB}_${timestamp}.sql"
    
    mkdir -p "$BACKUP_DIR"
    
    print_info "Criando backup em: $backup_file"
    
    docker-compose exec -T postgres pg_dump -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" > "$backup_file"
    
    if [ $? -eq 0 ]; then
        # Compactar backup
        gzip "$backup_file"
        print_success "Backup criado: ${backup_file}.gz"
        
        # Mostrar tamanho do backup
        local size=$(ls -lh "${backup_file}.gz" | awk '{print $5}')
        print_info "Tamanho do backup: $size"
        
        # Listar backups existentes
        echo ""
        echo -e "${CYAN}📁 Backups existentes:${NC}"
        ls -lht "$BACKUP_DIR"/*.gz 2>/dev/null || echo "  Nenhum backup anterior encontrado"
    else
        print_error "Falha ao criar backup"
        exit 1
    fi
}

# Limpar dados (CUIDADO!)
clean_data() {
    print_warning "⚠️  ATENÇÃO: Esta operação removerá TODOS os dados do banco!"
    print_warning "⚠️  Isso inclui volumes, containers e dados persistentes!"
    echo ""
    read -p "Tem certeza que deseja continuar? Digite 'CONFIRMAR' para prosseguir: " confirmation
    
    if [ "$confirmation" = "CONFIRMAR" ]; then
        print_info "Parando serviços..."
        docker-compose down
        
        print_info "Removendo volumes..."
        docker-compose down -v
        
        print_info "Removendo containers órfãos..."
        docker system prune -f
        
        print_success "Dados removidos com sucesso!"
        print_info "Execute './manage-db.sh start' para recriar o ambiente"
    else
        print_info "Operação cancelada"
    fi
}

# Mostrar ajuda
show_help() {
    print_header
    echo ""
    echo -e "${CYAN}📖 Comandos disponíveis:${NC}"
    echo ""
    echo -e "${GREEN}  start${NC}     - Inicia PostgreSQL e PgAdmin"
    echo -e "${GREEN}  stop${NC}      - Para os serviços"
    echo -e "${GREEN}  restart${NC}   - Reinicia os serviços"
    echo -e "${GREEN}  status${NC}    - Mostra informações de conexão"
    echo -e "${GREEN}  logs${NC}      - Mostra logs em tempo real"
    echo -e "${GREEN}  backup${NC}    - Cria backup do banco"
    echo -e "${GREEN}  connect${NC}   - Conecta via psql no terminal"
    echo -e "${GREEN}  clean${NC}     - Remove todos os dados (CUIDADO!)"
    echo -e "${GREEN}  help${NC}      - Mostra esta ajuda"
    echo ""
    echo -e "${YELLOW}📋 Exemplos de uso:${NC}"
    echo "  ./manage-db.sh start           # Iniciar ambiente"
    echo "  ./manage-db.sh status          # Ver informações"
    echo "  ./manage-db.sh backup          # Criar backup"
    echo "  ./manage-db.sh connect         # Abrir psql"
    echo ""
    echo -e "${BLUE}🔗 URLs importantes:${NC}"
    echo "  PgAdmin: http://localhost:8080"
    echo "  PostgreSQL: localhost:5432"
    echo ""
    echo -e "${RED}⚠️  Segurança:${NC}"
    echo "  - Altere as senhas padrão do arquivo .env"
    echo "  - Nunca commite o arquivo .env no git"
    echo "  - Use senhas fortes em produção"
}

# Main
main() {
    case "${1:-help}" in
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            restart_services
            ;;
        "status")
            show_status
            ;;
        "logs")
            show_logs
            ;;
        "backup")
            create_backup
            ;;
        "connect")
            connect_psql
            ;;
        "clean")
            clean_data
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_error "Comando inválido: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Executar função principal com todos os argumentos
main "$@"
