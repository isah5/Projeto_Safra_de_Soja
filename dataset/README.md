<!--
Integrantes: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067) | Orientador: Prof. Dr. Ivan Carlos Alcântara de Oliveira

Síntese do conteúdo deste arquivo: descreve as fontes de dados usadas no
projeto, os arquivos brutos já baixados em `dataset/raw/`, o dicionário de
variáveis planejado para a base final e as limitações conhecidas.

HISTÓRICO DE ALTERAÇÕES
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 | Criação do template de descrição do dataset
2026-09-24  | Download dos dados reais do IBGE/SIDRA (Tabela 1612) e do ONI/NOAA; documentação atualizada
2026-09-24 | Adicionados dados diários do INMET (45 estações do RS, 2000-2023), baixados manualmente via portal BDMEP
2026-09-25 | Estendido o range do IBGE e do ONI de 2000-2023 para 2000-2025 (a API do IBGE já publica dados até 2025); INMET segue em 2000-2023, atualização pendente
2026-09-25 | Estendido o INMET para 2000-2025 (download manual complementar via BDMEP, mesmas 45 estações, período 2024-2025); base completa nas 3 fontes
-->

# Dataset — descrição

## Fontes

| Fonte | Conteúdo | Período | Granularidade | Link | Status |
|---|---|---|---|---|---|
| IBGE/SIDRA — Tabela 1612 | Área plantada, área colhida, produção e rendimento médio de soja | 2000–2025 | Município (RS) | https://sidra.ibge.gov.br/tabela/1612 | ✅ baixado — `dataset/raw/ibge_sidra_1612_soja_rs_2000_2025.csv` |
| NOAA/CPC — ONI | Índice trimestral (médias móveis de 3 meses) do ENOS (El Niño/La Niña) | 1999–2025 | Trimestral (a agregar por safra) | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt | ✅ baixado — `dataset/raw/noaa_oni_1999_2025.csv` |
| INMET — BDMEP | Precipitação total diária e temperatura (máx/média/mín) diária, por estação automática | 2000-01-01 a 2025-12-31 | Estação meteorológica (diário) | https://bdmep.inmet.gov.br/ | ✅ baixado (manual, via portal BDMEP, em duas etapas) — `dataset/raw/inmet_estacoes_RS_consolidado_2000_2025.csv` (dados diários) + `dataset/raw/inmet_estacoes_metadados.csv` (lat/long/situação de cada estação) |
| Embrapa / CQFS-RS/SC | Recomendação de adubação fosfatada e potássica para soja, por classe de teor de P/K no solo | — | Classe de teor de P/K no solo (não por município) | https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1011192 | ✅ baixado — `dataset/raw/embrapa_tabela_2.3_interpretacao_teor_p_k.csv` + `dataset/raw/embrapa_tabela_2.4_recomendacao_p2o5_k2o_soja.csv` |

### Como os dados do IBGE foram obtidos

Via API pública do SIDRA (sem necessidade de token), tabela 1612, variáveis
109 (área plantada), 216 (área colhida), 214 (quantidade produzida) e 112
(rendimento médio), classificação 81 categoria 2713 (Soja em grão), para
todos os municípios do RS (`N6[N3[43]]`). A API do IBGE já publica dados até
2025 (a PAM de um ano costuma sair por volta de setembro do ano seguinte),
então usamos o range completo disponível, não só até 2023 como na primeira
versão desta base. Por limite de tamanho da API, a busca foi feita em duas
chamadas e depois unida:

```
https://servicodados.ibge.gov.br/api/v3/agregados/1612/periodos/2000-2023/variaveis/109|216|214|112?localidades=N6[N3[43]]&classificacao=81[2713]
https://servicodados.ibge.gov.br/api/v3/agregados/1612/periodos/2024-2025/variaveis/109|216|214|112?localidades=N6[N3[43]]&classificacao=81[2713]
```

(pedir os 26 anos de uma vez só retorna erro 500 do servidor do IBGE — é
mais confiável dividir a consulta.) O JSON bruto unido está em
`dataset/raw/ibge_sidra_1612_soja_rs_2000_2025_raw.json` e a versão já
tabulada (município × ano, uma linha por combinação) em
`dataset/raw/ibge_sidra_1612_soja_rs_2000_2025.csv` (12.922 linhas = 497
municípios × 26 safras). Valores ausentes (município sem produção de soja
naquele ano) aparecem como célula vazia.

### Como os dados do ONI foram obtidos

Arquivo ASCII oficial da NOAA/CPC (sem necessidade de API key):

```
https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
```

Cada linha é uma janela móvel de 3 meses (ex.: `DJF` = dez–jan–fev).
`dataset/raw/noaa_oni_1999_2025.csv` traz a série filtrada para 1999–2025
com colunas `seas`, `ano`, `total_sst`, `oni_anom` (o `oni_anom` é o índice
ONI propriamente dito). A NOAA já disponibiliza observações além de 2025,
mas cortamos em 2025 porque é o último ano com dado de safra do IBGE. O
notebook agrega essas janelas trimestrais em uma métrica por safra (média
do ONI nas janelas que cobrem out–mar de cada safra no RS).

### Como os dados do INMET foram obtidos

Baixados manualmente pelo portal BDMEP (https://bdmep.inmet.gov.br/), já que
a API automática (`apitempo.inmet.gov.br`) não respondeu nas tentativas via
script. Feito em **duas etapas**: primeiro 2000-01-01 a 2023-12-31, depois
(quando o IBGE e o ONI foram estendidos) o complemento 2024-01-01 a
2025-12-31, para as mesmas **45 estações automáticas** distribuídas pelo RS
(ex.: Porto Alegre, Rio Grande, Santa Maria, Uruguaiana, Bagé, Erechim,
Passo Fundo, Bento Gonçalves). O segundo download trouxe também dados de
outras ~37 estações novas da rede do INMET, que foram descartados para
manter o mesmo conjunto de 45 estações ao longo de toda a série — misturar
estações com históricos de tamanhos muito diferentes complicaria a
interpretação sem ganho real de cobertura.

- `dataset/raw/inmet_estacoes_metadados.csv` — uma linha por estação, com
  código, nome, latitude, longitude, altitude e situação (`Operante`,
  `Pane` ou `Desativada`).
- `dataset/raw/inmet_estacoes_RS_consolidado_2000_2025.csv` — 280.641
  linhas (estação × dia), 2000-01-01 a 2025-12-31, com precipitação total
  diária, temperatura máxima/média/mínima diária, e variáveis extras
  (pressão, umidade, ponto de orvalho, vento).

O notebook faz: (1) cálculo, para cada município, da estação mais próxima
(Haversine, usando as coordenadas de `inmet_estacoes_metadados.csv` e
`municipios_brasil_coords.csv`); (2) agregação dos dados diários por safra
(soma de precipitação, média de temperatura, na janela
semeadura–colheita); (3) tratamento de qualquer combinação estação-safra
com menos de 150 dos ~182 dias esperados (por `Pane` ou por a estação ainda
não estar instalada) como ausente, em vez de soma parcial enganosa.

### Como os dados de adubação fosfatada foram obtidos

O manual original da CQFS-RS/SC (2016), citado nas Referências do artigo, é
comercializado como livro impresso pela SBCS-Núcleo Regional Sul
(sbcs-nrs.org.br) e **não tem PDF gratuito oficial**. As mesmas tabelas de
recomendação (a base técnica é a mesma comissão/manual) são reproduzidas
livremente pela Embrapa em "Indicações Técnicas para a Cultura da Soja no
Rio Grande do Sul e em Santa Catarina", disponível sem custo no repositório
oficial Infoteca-e da Embrapa:
<https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/1011192>
(edição safras 2014/2015 e 2015/2016, que cita "MANUAL... (2004)" como
fonte primária das tabelas — a estrutura de classes e doses é a mesma usada
nas edições posteriores do manual, incluindo a de 2016).

Duas tabelas foram transcritas dessas páginas (Tabela 2.3 e Tabela 2.4 do
documento):

- `dataset/raw/embrapa_tabela_2.3_interpretacao_teor_p_k.csv` — classifica o
  teor de P e K do solo (mg/dm³) em Muito baixo/Baixo/Médio/Alto/Muito alto,
  variando conforme a classe textural do solo (argila) e a CTC a pH 7,0.
- `dataset/raw/embrapa_tabela_2.4_recomendacao_p2o5_k2o_soja.csv` — dose de
  P₂O₅ e K₂O (kg/ha) recomendada por classe de teor, para 1º e 2º cultivo
  após a adubação corretiva, considerando rendimento esperado de 2 t/ha
  (para rendimentos maiores, soma-se 15 kg/ha de P₂O₅ e 25 kg/ha de K₂O por
  tonelada adicional). Há também uma recomendação pontual de enxofre (20 kg
  S/ha quando o teor no solo é menor que 10 mg/dm³), registrada aqui como
  nota e não como tabela.

**Importante — isto não é uma série por município/ano**: ao contrário do
IBGE, ONI e INMET, esta fonte é uma **tabela de referência agronômica**
(dose recomendada em função do teor de P/K no solo), não uma medição
histórica. Não existe base pública de "quanto fósforo foi realmente
aplicado" por município e safra. Para usar isso no painel município–safra,
o grupo precisará de uma **hipótese simplificadora explícita** — por
exemplo, assumir uma classe de teor de solo típica por região do RS (com
base em levantamentos de fertilidade do solo já publicados, citando a
fonte) e aplicar a dose correspondente da Tabela 2.4 como atributo fixo ou
por região, deixando claro no artigo que é uma aproximação, não um dado
observado. Essa limitação já era esperada e está descrita no artigo
(seção 3.2, nota "Limitação a declarar explicitamente").

### Coordenadas dos municípios (auxiliar, para casar com o INMET)

O IBGE não expõe latitude/longitude na API usada para a Tabela 1612, mas o
notebook de análise exploratória precisa disso para achar a estação INMET
mais próxima de cada município. Usamos a base pública
[kelvins/municipios-brasileiros](https://github.com/kelvins/municipios-brasileiros)
(código IBGE → lat/long/UF, licença MIT), filtrada para o RS: `dataset/raw/municipios_brasil_coords.csv`.

## Chaves e formato final

- Chave primária da base final: `codigo_ibge_municipio` + `ano_safra`
- Arquivo(s) brutos: `dataset/raw/`
- Arquivo processado/final: `dataset/processed/painel_municipio_safra.csv` —
  gerado pelo notebook `notebooks/analise_exploratoria.ipynb`, junta IBGE +
  clima INMET (estação mais próxima) + ONI por safra. **Ainda não inclui**
  a adubação fosfatada (ver seção acima).

## Dicionário de variáveis

| Coluna | Descrição | Unidade | Fonte |
|---|---|---|---|
| `codigo_ibge_municipio` | Código IBGE do município | — | IBGE |
| `municipio` | Nome do município | — | IBGE |
| `ano_safra` | Ano da safra | ano | IBGE |
| `rendimento_kg_ha` | Rendimento médio (variável-alvo) | kg/ha | IBGE/SIDRA |
| `area_plantada_ha` | Área plantada | ha | IBGE/SIDRA |
| `producao_ton` | Produção total | toneladas | IBGE/SIDRA |
| `oni_media_safra` | ONI médio na janela semeadura–colheita | índice | NOAA/CPC |
| `precipitacao_total_safra_mm` | Soma da precipitação diária na janela semeadura–colheita (estação mais próxima) | mm | INMET |
| `temperatura_media_safra_c` | Média da temperatura média diária na janela semeadura–colheita | °C | INMET |
| `dose_p2o5_recomendada` | Dose de P₂O₅ recomendada por classe de solo | kg/ha | Embrapa / CQFS-RS/SC |
| ... | [completar conforme colunas finais geradas nos notebooks] | | |

Colunas brutas disponíveis em `inmet_estacoes_RS_consolidado_2000_2025.csv` (antes da
agregação por safra): `Codigo Estacao`, `Nome Estacao`, `Latitude`,
`Longitude`, `Altitude`, `Situacao`, `Data Medicao`, `PRECIPITACAO TOTAL,
DIARIO (AUT)(mm)`, `PRESSAO ATMOSFERICA MEDIA DIARIA (AUT)(mB)`,
`TEMPERATURA DO PONTO DE ORVALHO MEDIA DIARIA (AUT)(°C)`, `TEMPERATURA
MAXIMA, DIARIA (AUT)(°C)`, `TEMPERATURA MEDIA, DIARIA (AUT)(°C)`,
`TEMPERATURA MINIMA, DIARIA (AUT)(°C)`, `UMIDADE RELATIVA DO AR, MEDIA
DIARIA (AUT)(%)`, `UMIDADE RELATIVA DO AR, MINIMA DIARIA (AUT)(%)`, `VENTO,
RAJADA MAXIMA DIARIA (AUT)(m/s)`, `VENTO, VELOCIDADE MEDIA DIARIA
(AUT)(m/s)`. O arquivo usa `;` como separador e `,` como separador decimal
(padrão INMET) — atenção ao ler com pandas (`sep=';', decimal=','`).

## Limitações conhecidas

- Dados de adubação são **recomendações agronômicas por classe de solo**, não
  consumo real por produtor/município/ano.
- Municípios criados por desmembramento ao longo do período (2000–2025)
  podem ter séries históricas incompletas.
- A estação INMET usada por município é a mais próxima disponível, podendo
  não representar exatamente o microclima local.
- Várias estações do INMET aparecem como `Pane` em parte do período (falha
  de equipamento) — os dias correspondentes ficam com valor ausente na
  série e devem ser tratados como dado faltante, não como zero.
- A rede automática do INMET no RS começou a operar de forma escalonada
  (algumas estações só têm dados a partir de 2006-2007), então nem todo
  município tem cobertura climática completa desde 2000.

## Licença de uso dos dados originais

Todas as fontes são públicas (governamentais/institucionais). Citar a fonte
original ao reutilizar os dados.
