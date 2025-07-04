# Metadados do conjunto de dados: lista-aerodromos-privados-v2

**Publicado:** 28/04/2021 23h10
**Última modificação:** 07/04/2021 23h01

---

### Caracterização do conjunto de dados

- **Área temática:** Aeródromos
- **Conjunto de dados:** Lista de aeródromos privados V2
- **Nome da área de contato:** Gerência Técnica do Cadastro Aeroportuário - GTCA
- **E-mail de contato da área:** cadastro.aeroportuario@anac.gov.br
- **Periodicidade de atualização:** Aproximadamente a cada 40 dias (conforme ciclos de atualização de publicações aeronáuticas)
- **Descrição:** Dados cadastrais de aeródromos privados, que são aqueles aeródromos abertos ao tráfego aéreo de uso privativo.

---

### Visão geral

O Cadastro de Aeródromos é a informação oficial sobre a infraestrutura de aeródromos civis públicos e privados do Brasil.

O cadastro de aeródromos civis é mantido pela ANAC para inscrição dos aeródromos, instalações e equipamentos de auxílio à navegação aérea para atender à aviação civil.

De acordo com o art. 30 do Código Brasileiro de Aeronáutica (Lei nº 7.565, de 19 de dezembro de 1986), nenhum aeródromo civil poderá ser utilizado sem estar devidamente cadastrado.

**Algumas definições importantes:**

- **Aeródromo:** é toda área destinada a pouso, decolagem e movimentação de aeronaves. Os aeródromos podem ser classificados como públicos e privados.
- **Helipontos:** são os aeródromos destinados exclusivamente a helicópteros.
- **Heliportos:** são os helipontos públicos dotados de instalações e facilidades para apoio de operações a helicópteros e de embarque e desembarque de pessoas e cargas.
- **Helideque:** é uma estrutura construída para pousos e decolagens de helicópteros, instalada a bordo de plataformas marítimas ou em embarcações.

---

## Metadados

### Aeródromos Privados

| Campo                    | Descrição                                                                                                                                                                                                |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CÓDIGO OACI**          | Código de 4 letras utilizado internacionalmente para identificação de um aeródromo, conforme regras da OACI. No Brasil, são utilizados os códigos que iniciam com as letras SB, SD, SI, SJ, SN, SS e SW. |
| **CIAD**                 | Código de Identificação do Aeródromo, um identificador único de aeródromos civis (formato UF0000).                                                                                                       |
| **NOME**                 | Denominação do aeródromo.                                                                                                                                                                                |
| **MUNICÍPIO**            | Município onde se localiza o aeródromo.                                                                                                                                                                  |
| **UF**                   | Unidade da federação do município onde se localiza o aeródromo.                                                                                                                                          |
| **LATITUDE**             | Latitude do ponto de referência do aeródromo (graus, minutos, segundos, WGS-84).                                                                                                                         |
| **LONGITUDE**            | Longitude do ponto de referência do aeródromo (graus, minutos, segundos, WGS-84).                                                                                                                        |
| **ALTITUDE**             | Altitude do ponto de referência mais elevado na área de pouso, em metros.                                                                                                                                |
| **OPERAÇÃO DIURNA**      | Tipo de operação do período diurno para o qual o aeródromo está habilitado (VFR – Visual, IFR – Instrumento).                                                                                            |
| **OPERAÇÃO NOTURNA**     | Tipo de operação do período noturno para o qual o aeródromo está habilitado (VFR – Visual, IFR – Instrumento).                                                                                           |
| **DESIGNAÇÃO 1**         | Identificação da cabeceira da primeira pista de pouso e decolagem.                                                                                                                                       |
| **COMPRIMENTO 1**        | Comprimento da primeira pista de pouso e decolagem, em metros.                                                                                                                                           |
| **LARGURA 1**            | Largura da primeira pista de pouso e decolagem, em metros.                                                                                                                                               |
| **RESISTÊNCIA 1**        | Capacidade de suporte da superfície da primeira pista (ACN-PCN para > 5.700 kg; peso/pressão máxima para <= 5.700 kg).                                                                                   |
| **SUPERFÍCIE 1**         | Tipo de material da superfície da primeira pista.                                                                                                                                                        |
| **DESIGNAÇÃO 2**         | Identificação da cabeceira da segunda pista de pouso e decolagem.                                                                                                                                        |
| **COMPRIMENTO 2**        | Comprimento da segunda pista de pouso e decolagem, em metros.                                                                                                                                            |
| **LARGURA 2**            | Largura da segunda pista de pouso e decolagem, em metros.                                                                                                                                                |
| **RESISTÊNCIA 2**        | Capacidade de suporte da superfície da segunda pista.                                                                                                                                                    |
| **SUPERFÍCIE 2**         | Tipo de material da superfície da segunda pista.                                                                                                                                                         |
| **VALIDADE DO REGISTRO** | Data de validade do cadastro do aeródromo.                                                                                                                                                               |
| **PORTARIA DE REGISTRO** | Número e ano da última Portaria de cadastro do aeródromo (formato PAxxxx-yyyy).                                                                                                                          |
| **LINK PORTARIA**        | Link para acesso direto ao arquivo .pdf da portaria de cadastro.                                                                                                                                         |

### Helidecks

| Campo                                         | Descrição                                                                                                |
| :-------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| **CÓDIGO OACI**                               | Código de 4 letras utilizado internacionalmente para identificação de um aeródromo.                      |
| **CIAD**                                      | Código de Identificação do Aeródromo (formato UF0000).                                                   |
| **NOME**                                      | Denominação da área de pouso e decolagem de helicópteros.                                                |
| **ALTITUDE**                                  | Altitude do ponto mais elevado da área de pouso, em metros.                                              |
| **RESISTÊNCIA**                               | Capacidade de suporte da superfície, notificada pelo peso máximo permitido do helicóptero, em toneladas. |
| **COMPRIMENTO DO MAIOR HELICÓPTERO A OPERAR** | Maior dimensão do maior helicóptero cuja operação é prevista no helideck, em metros.                     |
| **VALIDADE DO CADASTRO**                      | Data de validade do cadastro do helideck.                                                                |
| **PORTARIA DE REGISTRO**                      | Número e ano da última Portaria de cadastro do helideck (formato PAxxxx-yyyy).                           |
| **LINK PORTARIA**                             | Link para acesso direto ao arquivo .pdf da portaria de cadastro.                                         |

### Helipontos

| Campo                        | Descrição                                                                                                |
| :--------------------------- | :------------------------------------------------------------------------------------------------------- |
| **CÓDIGO OACI**              | Código de 4 letras utilizado internacionalmente para identificação de um aeródromo.                      |
| **CIAD**                     | Código de Identificação do Aeródromo (formato UF0000).                                                   |
| **NOME**                     | Denominação da área de pouso e decolagem de helicópteros.                                                |
| **MUNICÍPIO**                | Município onde se localiza o heliponto.                                                                  |
| **UF**                       | Unidade da federação do município onde se localiza o heliponto.                                          |
| **TIPO**                     | Indica se a área de pouso está no nível do solo ou elevada.                                              |
| **LATITUDE**                 | Latitude de referência da área de pouso (graus, minutos, segundos, WGS-84).                              |
| **LONGITUDE**                | Longitude de referência da área de pouso (graus, minutos, segundos, WGS-84).                             |
| **ALTITUDE**                 | Altitude do ponto mais elevado da área de pouso, em metros.                                              |
| **OPERAÇÃO DIURNA**          | Tipo de operação do período diurno (VFR – Visual, IFR – Instrumento).                                    |
| **OPERAÇÃO NOTURNA**         | Tipo de operação do período noturno (VFR – Visual, IFR – Instrumento).                                   |
| **RAMPA DE APROXIMAÇÃO**     | Identificação da orientação para pouso e decolagem.                                                      |
| **FORMATO DA ÁREA DE POUSO** | Forma geométrica da área de aproximação final e decolagem.                                               |
| **DIMENSÕES**                | Comprimento e largura da área de aproximação final e decolagem.                                          |
| **RESISTÊNCIA**              | Capacidade de suporte da superfície, notificada pelo peso máximo permitido do helicóptero, em toneladas. |
| **SUPERFÍCIE**               | Tipo de material da superfície do pavimento.                                                             |
| **VALIDADE DO CADASTRO**     | Data de validade do cadastro do heliponto.                                                               |
| **PORTARIA DO CADASTRO**     | Número e ano da última Portaria de cadastro do heliponto (formato PAxxxx-yyyy).                          |
| **LINK PORTARIA**            | Link para acesso direto ao arquivo .pdf da portaria de cadastro.                                         |
