# Documentação: Atracações Portuárias da ANTAQ

Este documento descreve o conjunto de dados que contém informações detalhadas sobre as atracações em portos brasileiros, coletadas pela ANTAQ (Agência Nacional de Transportes Aquaviários).

---

### Exemplo dos Dados

| IDAtracacao | Porto Atracação | Coordenadas              | Município   | SGUF | Data Atracação      | Tipo de Navegação |
| :---------- | :-------------- | :----------------------- | :---------- | :--- | :------------------ | :---------------- |
| 1540851     | Belém           | -48.497777,-1.445278     | Belém       | PA   | 31/01/2025 08:15:00 | Longo Curso       |
| 1555062     | Paranaguá       | -48.505555,-25.502221    | Paranaguá   | PR   | 15/03/2025 09:20:00 | Cabotagem         |
| 1563179     | Paranaguá       | -48.505555,-25.502221    | Paranaguá   | PR   | 04/04/2025 08:20:00 | Cabotagem         |

---

### Descrição das Colunas

| Nome da Coluna              | Descrição Detalhada                                                                                     |
| :-------------------------- | :------------------------------------------------------------------------------------------------------ |
| **id_atracacao**            | **ID da Atracação:** Identificador único da operação de atracação.                                     |
| **cdtup**                   | **Código TUP:** Código do Terminal de Uso Privado.                                                     |
| **id_berco**                | **ID do Berço:** Identificador do berço onde ocorreu a atracação.                                      |
| **berco**                   | **Berço:** Nome ou número do berço de atracação.                                                       |
| **porto_atracacao**         | **Porto de Atracação:** Nome do porto onde ocorreu a atracação.                                        |
| **coordenadas**             | **Coordenadas:** Coordenadas geográficas no formato "longitude,latitude".                              |
| **latitude**                | **Latitude:** Latitude extraída das coordenadas.                                                       |
| **longitude**               | **Longitude:** Longitude extraída das coordenadas.                                                     |
| **apelido_instalacao**      | **Apelido da Instalação:** Nome alternativo da instalação portuária.                                   |
| **complexo_portuario**      | **Complexo Portuário:** Nome do complexo portuário ao qual pertence.                                   |
| **tipo_autoridade**         | **Tipo da Autoridade:** Tipo da autoridade portuária (ex: Porto Organizado).                          |
| **data_atracacao**          | **Data de Atracação:** Data e hora quando a embarcação atracou.                                        |
| **data_chegada**            | **Data de Chegada:** Data e hora de chegada da embarcação ao porto.                                    |
| **data_desatracacao**       | **Data de Desatracação:** Data e hora quando a embarcação desatracou.                                  |
| **data_inicio_operacao**    | **Data de Início da Operação:** Data e hora de início das operações de carga/descarga.                |
| **data_termino_operacao**   | **Data de Término da Operação:** Data e hora de término das operações de carga/descarga.              |
| **ano**                     | **Ano:** Ano da operação de atracação.                                                                 |
| **mes**                     | **Mês:** Mês da operação de atracação.                                                                 |
| **tipo_operacao**           | **Tipo de Operação:** Tipo da operação realizada (ex: Marinha).                                        |
| **tipo_navegacao**          | **Tipo de Navegação:** Tipo de navegação da atracação (ex: Longo Curso, Cabotagem).                   |
| **nacionalidade_armador**   | **Nacionalidade do Armador:** Código da nacionalidade do armador da embarcação.                        |
| **flag_mc_operacao**        | **Flag MC Operação:** Flag indicando se é operação de movimentação de carga.                          |
| **terminal**                | **Terminal:** Nome do terminal onde ocorreu a atracação.                                               |
| **municipio**               | **Município:** Município onde está localizado o porto.                                                 |
| **uf**                      | **UF:** Unidade Federativa onde está localizado o porto.                                               |
| **sguf**                    | **Sigla UF:** Sigla da Unidade Federativa.                                                             |
| **regiao_geografica**       | **Região Geográfica:** Região geográfica do Brasil.                                                    |
| **regiao_hidrografica**     | **Região Hidrográfica:** Região hidrográfica onde está localizado o porto.                            |
| **instalacao_em_rio**       | **Instalação em Rio:** Indica se a instalação portuária está localizada em rio.                       |
| **numero_capitania**        | **Número da Capitania:** Número da Capitania dos Portos responsável.                                   |
| **numero_imo**              | **Número IMO:** Número IMO (International Maritime Organization) da embarcação.                        |

---

### Tipos de Navegação

#### 🌊 Longo Curso
- **Descrição:** Navegação entre portos brasileiros e estrangeiros
- **Características:** Transporte internacional de cargas e passageiros
- **Exemplos:** Exportação de commodities, importação de produtos

#### 🚢 Cabotagem
- **Descrição:** Navegação entre portos nacionais
- **Características:** Transporte doméstico de cargas e passageiros
- **Exemplos:** Transporte de contêineres entre Santos e Rio de Janeiro

#### ⚓ Interior
- **Descrição:** Navegação em rios e hidrovias interiores
- **Características:** Transporte fluvial de cargas
- **Exemplos:** Transporte no Rio Amazonas, Tietê-Paraná

---

### Tipos de Autoridade Portuária

#### 🏛️ Porto Organizado
- **Descrição:** Portos administrados pelas Autoridades Portuárias
- **Características:** Infraestrutura pública com múltiplos operadores
- **Exemplos:** Santos, Rio de Janeiro, Paranaguá

#### 🏢 Terminal de Uso Privado (TUP)
- **Descrição:** Terminais operados por empresas privadas
- **Características:** Uso próprio ou de terceiros mediante autorização
- **Exemplos:** Terminais de mineração, petroquímicos

---

### Informações sobre a Fonte

- **Órgão Responsável:** ANTAQ (Agência Nacional de Transportes Aquaviários)
- **Sistema:** Estatística da Navegação Interior e Cabotagem
- **Ano de Referência:** 2025
- **URL da Fonte:** https://web3.antaq.gov.br/ea/txt/2025Atracacao.zip
- **Formato:** Arquivo ZIP contendo TXT delimitado por ponto e vírgula
- **Atualização:** Dados atualizados periodicamente pela ANTAQ

---

### Características dos Dados

- **Total de Atracações:** 36.694 atracações (dados de 2025)
- **Cobertura Temporal:** Dados do ano de 2025
- **Cobertura Geográfica:** Todo o território nacional
- **Coordenadas:** 36.692 atracações com coordenadas geográficas (99,99%)
- **Estados Abrangidos:** Todos os estados costeiros e com hidrovias

---

### Distribuição por Região

#### 🌊 Top 5 Portos por Atracações
1. **Brasil Logística Offshore e Estaleiro Naval:** 3.320 atracações
2. **Rio de Janeiro:** 1.954 atracações  
3. **Belém:** 1.833 atracações
4. **Santos:** 1.651 atracações
5. **Santarém:** 1.142 atracações

#### 📊 Tipos de Navegação Mais Frequentes
- **Cabotagem:** Transporte doméstico entre portos brasileiros
- **Longo Curso:** Transporte internacional
- **Interior:** Navegação fluvial e lacustre

---

### Processamento dos Dados

Durante o processamento pelo scraper:
1. **Download:** Baixa arquivo ZIP da ANTAQ
2. **Extração:** Extrai arquivo TXT do ZIP
3. **Parsing:** Processa CSV delimitado por ponto e vírgula
4. **Transformação:** Converte datas para formato ISO
5. **Geocodificação:** Extrai latitude e longitude das coordenadas
6. **Validação:** Verifica integridade dos dados obrigatórios
7. **Carregamento:** Salva em lotes no banco PostgreSQL

---

### Estrutura do Arquivo Original

- **Formato:** TXT delimitado por ponto e vírgula (;)
- **Encoding:** UTF-8 com BOM
- **Cabeçalho:** Primeira linha contém nomes das colunas
- **Registros:** Uma linha por atracação
- **Tamanho:** ~12 MB comprimido, ~37K registros

---

### Casos de Uso

#### 📈 Análises Econômicas
- Monitoramento do fluxo de cargas nos portos
- Análise de sazonalidade do transporte aquaviário
- Identificação de gargalos logísticos

#### 🗺️ Estudos Geográficos
- Mapeamento da infraestrutura portuária nacional
- Análise da distribuição espacial do comércio
- Planejamento de investimentos em logística

#### 📊 Business Intelligence
- Dashboards de movimentação portuária
- Relatórios de performance de terminais
- Análise de tendências do setor aquaviário

#### 🔍 Pesquisa Acadêmica
- Estudos sobre economia marítima
- Análise de cadeias logísticas
- Pesquisas sobre sustentabilidade portuária

---

### Limitações e Considerações

- **Período:** Dados limitados ao ano de 2025
- **Completude:** Alguns campos podem estar vazios conforme disponibilidade
- **Precisão:** Coordenadas fornecidas pela fonte original
- **Atualizações:** Dados dependem da atualização pela ANTAQ
- **Escopo:** Foco em atracações, não incluindo outras operações portuárias
