# Documentação: Municípios das Zonas Fiscais Especiais da SUFRAMA

Este documento descreve o conjunto de dados que identifica os municípios brasileiros pertencentes às Zonas Fiscais Especiais administradas pela SUFRAMA (Superintendência da Zona Franca de Manaus).

---

### Exemplo dos Dados

| CD_MUN  | NM_MUN           | TIPO_ZONA               |
| :------ | :--------------- | :---------------------- |
| 1302603 | Manaus           | ZONA FRANCA DE MANAUS   |
| 1303569 | Rio Preto da Eva | ZONA FRANCA DE MANAUS   |
| 1301902 | Itacoatiara      | ZONA FRANCA DE MANAUS   |
| 1200104 | Brasileia        | ÁREAS DE LIVRE COMÉRCIO |
| 1200252 | Epitaciolândia   | ÁREAS DE LIVRE COMÉRCIO |

---

### Descrição das Colunas

| Nome da Coluna | Descrição Detalhada                                                                                                                              |
| :-------------| :----------------------------------------------------------------------------------------------------------------------------------------------- |
| **CD_MUN**    | **Código do Município:** Identificador único de 7 dígitos do IBGE para o município.                                                           |
| **NM_MUN**    | **Nome do Município:** Nome oficial do município que faz parte da zona fiscal especial.                                                        |
| **TIPO_ZONA** | **Tipo da Zona Fiscal:** Classificação da zona fiscal especial. Pode ser `'ZONA FRANCA DE MANAUS'` ou `'ÁREAS DE LIVRE COMÉRCIO'`.          |

---

### Tipos de Zonas Fiscais Especiais

#### 🏗️ Zona Franca de Manaus
- **Descrição:** Área de livre comércio de importação e exportação e de incentivos fiscais especiais
- **Localização:** Região metropolitana de Manaus
- **Municípios incluídos:**
  - Manaus (1302603)
  - Rio Preto da Eva (1303569) 
  - Itacoatiara (1301902)

#### 🛒 Áreas de Livre Comércio (ALC)
- **Descrição:** Áreas de fronteira com regime tributário especial para desenvolvimento regional
- **Características:** Localizadas em regiões fronteiriças para fomentar o desenvolvimento local
- **Municípios incluídos:**
  - **Acre:** Brasileia, Epitaciolândia, Cruzeiro do Sul
  - **Amapá:** Macapá, Santana
  - **Amazonas:** Tabatinga
  - **Rondônia:** Guajará-Mirim
  - **Roraima:** Boa Vista, Bonfim

---

### Informações sobre a Fonte

- **Órgão Responsável:** IBGE (Instituto Brasileiro de Geografia e Estatística)
- **Base de Dados:** Organização do Território / Estrutura Territorial / SUFRAMA
- **Ano de Referência:** 2022
- **URL da Fonte:** https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/SUFRAMA/2022/Municipios_SUFRAMA.xlsx
- **Formato:** Arquivo Excel (.xlsx)
- **Periodicidade:** Atualização irregular conforme mudanças na legislação

---

### Características dos Dados

- **Total de Municípios:** 11 municípios
- **Cobertura Geográfica:** Região Norte do Brasil
- **Estados Abrangidos:** AC, AM, AP, RO, RR
- **Distribuição:**
  - Zona Franca de Manaus: 3 municípios
  - Áreas de Livre Comércio: 8 municípios

---

### Estrutura do Arquivo Original

O arquivo Excel possui um formato especial:
- **Linha 1:** Cabeçalhos (TIPO, CODMUN, MUNICÍPIO, CODMUN, MUNICÍPIO, ...)
- **Linha 2:** ZONA FRANCA DE MANAUS com códigos e nomes dos municípios
- **Linha 3:** ÁREAS DE LIVRE COMÉRCIO com códigos e nomes dos municípios
- **Linhas 4-8:** Continuação das ÁREAS DE LIVRE COMÉRCIO com mais municípios
- **Colunas:** Múltiplas colunas com códigos e nomes alternados