# Documentação: Metadados de Municípios

Este documento descreve as colunas presentes no conjunto de dados de municípios, comumente utilizado pelo IBGE (Instituto Brasileiro de Geografia e Estatística). A estrutura visa organizar as localidades brasileiras em diferentes níveis geográficos.

---

### Exemplo dos Dados

| CD_MUN  | NM_MUN         | CD_RGI | NM_RGI   | CD_RGINT | NM_RGINT  | CD_UF | NM_UF | SIGLA_UF | CD_REGIA | NM_REGIA | SIGLA_RG | AREA_KM2 |
| :------ | :------------- | :----- | :------- | :------- | :-------- | :---- | :---- | :------- | :------- | :------- | :------- | :------- |
| 1500909 | Augusto Corrêa | 150005 | Bragança | 1502     | Castanhal | 15    | Pará  | PA       | 1        | Norte    | N        | 1099,580 |
| 1501709 | Bragança       | 150005 | Bragança | 1502     | Castanhal | 15    | Pará  | PA       | 1        | Norte    | N        | 2124,735 |

---

### Descrição das Colunas

| Nome da Coluna | Descrição Detalhada                                                                                                        |
| :------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **CD_MUN**     | **Código do Município:** Código numérico único de 7 dígitos atribuído pelo IBGE para identificar cada município no Brasil. |
| **NM_MUN**     | **Nome do Município:** Nome oficial do município.                                                                          |
| **CD_RGI**     | **Código da Região Geográfica Imediata:** Código do agrupamento de municípios próximos com uma cidade polo principal.      |
| **NM_RGI**     | **Nome da Região Geográfica Imediata:** Nome do agrupamento de municípios próximos.                                        |
| **CD_RGINT**   | **Código da Região Geográfica Intermediária:** Código do agrupamento de várias Regiões Geográficas Imediatas.              |
| **NM_RGINT**   | **Nome da Região Geográfica Intermediária:** Nome do agrupamento de Regiões Geográficas Imediatas.                         |
| **CD_UF**      | **Código da Unidade da Federação:** Código numérico do estado.                                                             |
| **NM_UF**      | **Nome da Unidade da Federação:** Nome por extenso do estado.                                                              |
| **SIGLA_UF**   | **Sigla da Unidade da Federação:** Sigla de duas letras do estado.                                                         |
| **CD_REGIA**   | **Código da Região:** Código da grande região do Brasil (ex: 1 para Norte, 2 para Nordeste).                               |
| **NM_REGIA**   | **Nome da Região:** Nome da grande região do Brasil (Norte, Nordeste, Sudeste, Sul, Centro-Oeste).                         |
| **SIGLA_RG**   | **Sigla da Região:** Sigla da grande região (N, NE, SE, S, CO).                                                            |
| **AREA_KM2**   | **Área em Quilômetros Quadrados:** Área territorial oficial do município em km².                                           |
