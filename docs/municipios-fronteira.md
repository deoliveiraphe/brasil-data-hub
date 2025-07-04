# Documentação: Municípios da Faixa de Fronteira e Cidades Gêmeas

Este documento descreve as colunas do conjunto de dados que identifica os municípios brasileiros localizados na Faixa de Fronteira, suas áreas e a classificação como Cidades Gêmeas.

---

### Exemplo dos Dados

| CD_MUN  | NM_MUN                | ... | AREA_TOT | TOCA_LIM | AREA_INT | PORC_INT | FAIXA_SEDE | CID_GEMEA |
| :------ | :-------------------- | :-- | :------- | :------- | :------- | :------- | :--------- | :-------- |
| 1100015 | Alta Floresta D'Oeste | ... | 7067,127 | SIM      | 7067,127 | 100,000  | sim        |           |

_(... colunas geográficas omitidas por brevidade)_

---

### Descrição das Colunas

| Nome da Coluna | Descrição Detalhada                                                                                                                                                |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CD_MUN**     | **Código do Município:** Identificador único de 7 dígitos do IBGE para o município.                                                                                |
| **NM_MUN**     | **Nome do Município:** Nome oficial do município.                                                                                                                  |
| **CD_RGI**     | **Código da Região Geográfica Imediata:** Código do agrupamento de municípios próximos.                                                                            |
| **NM_RGI**     | **Nome da Região Geográfica Imediata:** Nome do agrupamento de municípios próximos.                                                                                |
| **CD_RGINT**   | **Código da Região Geográfica Intermediária:** Código do agrupamento de Regiões Imediatas.                                                                         |
| **NM_RGINT**   | **Nome da Região Geográfica Intermediária:** Nome do agrupamento de Regiões Imediatas.                                                                             |
| **CD_UF**      | **Código da Unidade da Federação:** Código numérico do estado.                                                                                                     |
| **NM_UF**      | **Nome da Unidade da Federação:** Nome por extenso do estado.                                                                                                      |
| **SIGLA_UF**   | **Sigla da Unidade da Federação:** Sigla de duas letras do estado.                                                                                                 |
| **CD_REGIAO**  | **Código da Região:** Código da grande região do Brasil.                                                                                                           |
| **NM_REGIAO**  | **Nome da Região:** Nome da grande região do Brasil.                                                                                                               |
| **SIGLA_RG**   | **Sigla da Região:** Sigla da grande região.                                                                                                                       |
| **AREA_TOT**   | **Área Total:** Área territorial total do município em km².                                                                                                        |
| **TOCA_LIM**   | **Toca o Limite:** Indica se o território do município toca a fronteira internacional (`SIM` ou `NÃO`).                                                            |
| **AREA_INT**   | **Área na Faixa de Fronteira:** Área do município, em km², que está contida dentro da Faixa de Fronteira.                                                          |
| **PORC_INT**   | **Porcentagem na Faixa de Fronteira:** Percentual da área do município que está contida na Faixa de Fronteira.                                                     |
| **FAIXA_SEDE** | **Sede na Faixa:** Indica se a sede (área urbana principal) do município está localizada dentro da Faixa de Fronteira.                                             |
| **CID_GEMEA**  | **Cidade Gêmea:** Indica se o município é classificado como uma "Cidade Gêmea" (cidade que faz fronteira e tem forte interação com uma cidade de um país vizinho). |
