# Metadados do conjunto de dados: lista-aerodromos-publicos-v2

**Publicado:** 04/05/2021 11h23
**Última modificação:** 29/04/2021 15h01

---

### Caracterização do conjunto de dados

- **Área temática:** Aeródromos
- **Conjunto de dados:** Lista de aeródromos públicos V2
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

### Metadados dos Aeródromos Públicos

| Campo                    | Descrição                                                                                                                                                                                                                                                                                                                |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CÓDIGO OACI**          | Código de 4 letras utilizado internacionalmente para identificação de um aeródromo, conforme regras da Organização de Aviação Civil Internacional (OACI). No Brasil, são utilizados os códigos que iniciam com as letras SB, SD, SI, SJ, SN, SS e SW.                                                                    |
| **CIAD**                 | O Código de Identificação do Aeródromo se trata de um identificador único de aeródromos civis, e é formado pela junção de dois caracteres e quatro dígitos, sendo que os caracteres são referentes à unidade da federação onde o aeródromo se localiza e os dígitos são atribuídos de forma sequencial (formato UF0000). |
| **NOME**                 | Denominação do aeródromo.                                                                                                                                                                                                                                                                                                |
| **MUNICÍPIO**            | Município onde se localiza o aeródromo, considerando as coordenadas de referência do mesmo.                                                                                                                                                                                                                              |
| **UF**                   | Unidade da federação do município onde se localiza o aeródromo.                                                                                                                                                                                                                                                          |
| **MUNICÍPIO SERVIDO**    | Município principal servido pelo aeródromo.                                                                                                                                                                                                                                                                              |
| **UF SERVIDO**           | Unidade da federação do município servido.                                                                                                                                                                                                                                                                               |
| **LATITUDE**             | Latitude do ponto de referência do aeródromo. A coordenada geográfica é fornecida em graus, minutos e segundos, o sistema de referência é WGS-84.                                                                                                                                                                        |
| **LONGITUDE**            | Longitude do ponto de referência do aeródromo. A coordenada geográfica é fornecida em graus, minutos e segundos, o sistema de referência é WGS-84.                                                                                                                                                                       |
| **ALTITUDE**             | Altitude do ponto de referência mais elevado na área de pouso, em metros.                                                                                                                                                                                                                                                |
| **OPERAÇÃO DIURNA**      | Tipo de operação do período diurno para o qual o aeródromo está habilitado, considerando as regras de voo (VFR – Visual, IFR – Instrumento).                                                                                                                                                                             |
| **OPERAÇÃO NOTURNA**     | Tipo de operação do período noturno para o qual o aeródromo está habilitado, considerando as regras de voo (VFR – Visual, IFR – Instrumento).                                                                                                                                                                            |
| **DESIGNAÇÃO 1**         | Identificação de cada uma das cabeceiras da primeira pista de pouso e decolagem, que é definida conforme orientação magnética da pista.                                                                                                                                                                                  |
| **COMPRIMENTO 1**        | Comprimento da primeira pista de pouso e decolagem, considerando a porção desta disponível para passagem trânsito das aeronaves em condições normais.                                                                                                                                                                    |
| **LARGURA 1**            | Largura da primeira pista de pouso e decolagem, considerando a distância lateral na qual uma aeronave pode transitar em condições normais de operação.                                                                                                                                                                   |
| **RESISTÊNCIA 1**        | Capacidade de suporte da superfície da primeira pista de pouso e decolagem. A resistência de pavimentos para aeronaves com peso > 5.700 kg deve ser divulgada pelo método ACN-PCN; para peso <= 5.700 kg, deve-se informar o peso máximo e a pressão máxima dos pneus.                                                   |
| **SUPERFÍCIE 1**         | Tipo de material da superfície da primeira pista de pouso e decolagem.                                                                                                                                                                                                                                                   |
| **DESIGNAÇÃO 2**         | Identificação de cada uma das cabeceiras da segunda pista de pouso e decolagem.                                                                                                                                                                                                                                          |
| **COMPRIMENTO 2**        | Comprimento da segunda pista de pouso e decolagem.                                                                                                                                                                                                                                                                       |
| **LARGURA 2**            | Largura da segunda pista de pouso e decolagem.                                                                                                                                                                                                                                                                           |
| **RESISTÊNCIA 2**        | Capacidade de suporte da superfície da segunda pista. Mesmas regras da RESISTÊNCIA 1.                                                                                                                                                                                                                                    |
| **SUPERFÍCIE 2**         | Tipo de material da superfície da segunda pista de pouso e decolagem.                                                                                                                                                                                                                                                    |
| **SITUAÇÃO**             | Indicação de eventual medida administrativa aplicada pela ANAC ao aeródromo, em geral constituindo-se em algum tipo de restrição operacional.                                                                                                                                                                            |
| **VALIDADE DO CADASTRO** | Data de validade do cadastro do aeródromo.                                                                                                                                                                                                                                                                               |
| **PORTARIA DE CADASTRO** | Número e ano da última Portaria de cadastro do aeródromo dentro da validade (formato PAxxxx-yyyy).                                                                                                                                                                                                                       |
| **LINK PORTARIA**        | Link para acesso direto ao arquivo .pdf da portaria de cadastro do aeródromo.                                                                                                                                                                                                                                            |
