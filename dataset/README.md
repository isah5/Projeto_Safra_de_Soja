<!--
Integrantes:
Orientador:

Síntese do conteúdo deste arquivo: descreve as fontes de dados usadas no
projeto, os arquivos brutos já baixados em `dataset/raw/`, o dicionário de
variáveis planejado para a base final e as limitações conhecidas.

HISTÓRICO DE ALTERAÇÕES
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 |                  | Criação do template de descrição do dataset
2026-09-24 |                   | Download dos dados reais do IBGE/SIDRA (Tabela 1612) e do ONI/NOAA; documentação atualizada
2026-09-24 |                 | Adicionados dados diários do INMET (45 estações do RS, 2000-2023), baixados manualmente via portal BDMEP
2026-09-25 |                 | Estendido o range do IBGE e do ONI de 2000-2023 para 2000-2025 (a API do IBGE já publica dados até 2025); INMET segue em 2000-2023, atualização pendente
2026-09-25 |                 | Estendido o INMET para 2000-2025 (download manual complementar via BDMEP, mesmas 45 estações, período 2024-2025); base completa nas 3 fontes
2026-10-22 |                 | Adicionado o arquivo processado de clima por subperíodo (estação × safra), gerado na Etapa 2 da modelagem
2026-10-22 |                 | Adicionada a tabela de regiões dos municípios do RS (API de localidades do IBGE)
2026-10-22 |                 | Removido o JSON bruto do IBGE (não usado; o CSV tabulado é a fonte dos notebooks); tabelas da Embrapa passam a ser usadas na recomendação de adubação; adicionado o arquivo de recomendação da safra 2026
2026-10-23 |                 | Adicionado o clima diário do NASA POWER (87 células da grade que cobrem os municípios do RS, 2000-2025), baixado por `dataset/baixar_nasa_power.py`; adicionados os arquivos processados de balanço hídrico das estações (Etapa 4) e de clima do NASA POWER por célula e safra (Etapa 5)
-->

# Dataset — descrição

## Fontes

| Fonte | Conteúdo | Período | Granularidade | Link | Status |
|---|---|---|---|---|---|
| IBGE/SIDRA — Tabela 1612 | Área plantada, área colhida, produção e rendimento médio de soja | 2000–2025 | Município (RS) | https://sidra.ibge.gov.br/tabela/1612 | ✅ baixado — `dataset/raw/ibge_sidra_1612_soja_rs_2000_2025.csv` |
| NOAA/CPC — ONI | Índice trimestral (médias móveis de 3 meses) do ENOS (El Niño/La Niña) | 1999–2025 | Trimestral (a agregar por safra) | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt | ✅ baixado — `dataset/raw/noaa_oni_1999_2025.csv` |
| INMET — BDMEP | Precipitação total diária e temperatura (máx/média/mín) diária, por estação automática | 2000-01-01 a 2025-12-31 | Estação meteorológica (diário) | https://bdmep.inmet.gov.br/ | ✅ baixado (manual, via portal BDMEP, em duas etapas) — `dataset/raw/inmet_estacoes_RS_consolidado_2000_2025.csv` (dados diários) + `dataset/raw/inmet_estacoes_metadados.csv` (lat/long/situação de cada estação) |
| NASA POWER (NASA/LaRC) | Chuva, temperatura média/máxima/mínima, ponto de orvalho e umidade relativa média diários (reanálise MERRA-2) | 2000–2025 (só out–mai) | Célula da grade de 0,5° × 0,625° (diário) | https://power.larc.nasa.gov/ | ✅ baixado (script `dataset/baixar_nasa_power.py`) — `dataset/raw/nasa_power_rs_2000_2025.csv` + `dataset/raw/nasa_power_celulas_municipios_rs.csv` |
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
mais confiável dividir a consulta.) As respostas foram unidas e tabuladas
(município × ano, uma linha por combinação) em
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

### Como os dados do NASA POWER foram obtidos

Pela API pública de dados diários do NASA POWER (sem necessidade de token), comunidade
`AG` (agroclimatologia), com o script `dataset/baixar_nasa_power.py` (rodar a partir da
raiz do repositório: `python dataset/baixar_nasa_power.py`). Exemplo de consulta para
uma célula:

```
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR,T2M,T2M_MAX,T2M_MIN,T2MDEW,RH2M&community=AG&latitude=-28.5&longitude=-52.5&start=20000101&end=20251231&format=JSON
```

A grade do NASA POWER (MERRA-2) tem células de 0,5° de latitude × 0,625° de longitude
(~50 km), e todos os pontos de uma célula recebem o mesmo valor (verificado consultando
pontos diferentes da mesma célula). Por isso, cada município do RS é associado à célula
que contém a sua coordenada (`municipios_brasil_coords.csv`, filtrado pela UF 43), e cada
célula é baixada uma única vez: os 497 municípios caem em **87 células**. Só os meses de
outubro a maio (janela da safra) são guardados. Baixado em 2026-10-23, sem nenhum valor
ausente.

- `dataset/raw/nasa_power_celulas_municipios_rs.csv` — município → célula
  (`codigo_ibge_municipio`, `lat_celula`, `lon_celula`).
- `dataset/raw/nasa_power_rs_2000_2025.csv` — 550.275 linhas (célula × dia), com
  `chuva_mm` (PRECTOTCORR, precipitação corrigida), `t2m_c`, `tmax_c`, `tmin_c`,
  `tdew_c` (ponto de orvalho) e `rh2m_pct` (umidade relativa média). O NASA POWER não
  fornece a umidade relativa mínima; o notebook da Etapa 5 a estima pelo ponto de
  orvalho e pela temperatura máxima (FAO-56).

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
aplicado" por município e safra. Por isso, **as tabelas não entram como
variável de previsão** (uma dose fixa por município não acrescenta
informação ao modelo, que já capta o que é fixo de cada município pelo
patamar). Elas são usadas na **aplicação do modelo**
(`notebooks/modelagem_etapa4.ipynb`, seção 11): o rendimento esperado de
cada município é combinado com a Tabela 2.4 para gerar a dose de P₂O₅ e K₂O
para **cada uma das cinco classes de teor**, e a Tabela 2.3 orienta o
produtor a identificar a sua classe pela própria análise de solo. Nenhuma
suposição sobre o solo dos municípios é feita.

### Coordenadas dos municípios (auxiliar, para casar com o INMET)

O IBGE não expõe latitude/longitude na API usada para a Tabela 1612, mas o
notebook de análise exploratória precisa disso para achar a estação INMET
mais próxima de cada município. Usamos a base pública
[kelvins/municipios-brasileiros](https://github.com/kelvins/municipios-brasileiros)
(código IBGE → lat/long/UF, licença MIT), filtrada para o RS: `dataset/raw/municipios_brasil_coords.csv`.

### Regiões dos municípios (auxiliar, para métricas por região)

Para calcular o erro do modelo por região, cada município do RS foi associado à sua
microrregião, mesorregião, região geográfica imediata e intermediária, pela API pública
de localidades do IBGE (sem token):

```
https://servicodados.ibge.gov.br/api/v1/localidades/estados/43/municipios
```

Salvo em `dataset/raw/ibge_municipios_rs_regioes.csv` (497 municípios, colunas
`codigo_ibge_municipio`, `municipio`, `microrregiao`, `mesorregiao`,
`regiao_imediata`, `regiao_intermediaria`). Baixado em 2026-10-22.

## Chaves e formato final

- Chave primária da base final: `codigo_ibge_municipio` + `ano_safra`
- Arquivo(s) brutos: `dataset/raw/`
- Arquivo processado/final: `dataset/processed/painel_municipio_safra.csv` —
  gerado pelo notebook `notebooks/analise_exploratoria.ipynb`, junta IBGE +
  clima INMET (estação mais próxima) + ONI por safra. Não inclui a
  adubação fosfatada (ver seção acima).
- `dataset/processed/clima_subperiodos_estacao_safra.csv` — gerado por
  `notebooks/modelagem_etapa2.ipynb` a partir do INMET diário; uma linha por
  estação × safra (chave `codigo_estacao` + `ano_safra`, que liga ao painel), com
  chuva acumulada em out–nov, dez–fev, mar e abr–mai e, para dez–fev, maior
  sequência de dias secos (< 1 mm), dias com máxima ≥ 32 °C, média da máxima e
  média da umidade relativa mínima. Valor ausente quando a estação tem dado em
  menos de 80% dos dias do subperíodo. Usado por `notebooks/modelagem_etapa3.ipynb`
  e `notebooks/modelagem_etapa4.ipynb`.
- `dataset/processed/balanco_hidrico_estacao_safra.csv` — gerado por
  `notebooks/modelagem_etapa4.ipynb` a partir do INMET diário; uma linha por estação ×
  safra, com o déficit hídrico de dez–fev (CAD de 50, 75 e 100 mm; `deficit_dez_fev`
  usa 75 mm), o balanço chuva − ETo e a ETo acumulados em dez–fev. Usado por
  `notebooks/modelagem_etapa5_nasa_power.ipynb`.
- `dataset/processed/clima_nasa_power_celula_safra.csv` — gerado por
  `notebooks/modelagem_etapa5_nasa_power.ipynb` a partir do NASA POWER diário; uma linha
  por célula × safra (chave `celula` + `ano_safra`; a célula de cada município está em
  `dataset/raw/nasa_power_celulas_municipios_rs.csv`), com as mesmas variáveis do clima
  por subperíodo e do balanço hídrico das estações.
- `dataset/processed/recomendacao_adubacao_safra2026.csv` — gerado por
  `notebooks/modelagem_etapa4.ipynb`; resultado da aplicação do modelo, não
  insumo. Uma linha por município × classe de teor de P/K no solo (431
  municípios × 5 classes), com o rendimento esperado para a safra 2026 (média
  de 2021–2025) e a dose de P₂O₅ e K₂O (kg/ha) no 1º e 2º cultivo.

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
- O NASA POWER é uma reanálise em grade (~50 km), não uma medição local: municípios na
  mesma célula recebem o mesmo clima, e extremos locais tendem a ser suavizados. A
  umidade relativa mínima é estimada, não medida.

## Licença de uso dos dados originais

Todas as fontes são públicas (governamentais/institucionais). Citar a fonte
original ao reutilizar os dados.
