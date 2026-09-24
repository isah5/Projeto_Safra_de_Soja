<!--
Grupo: [preencher] | Integrantes: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067) | Orientador: Prof. Dr. Ivan Carlos Alcântara de Oliveira

Síntese do conteúdo deste arquivo: descreve as fontes de dados usadas no
projeto, os arquivos brutos já baixados em `dataset/raw/`, o dicionário de
variáveis planejado para a base final e as limitações conhecidas.

HISTÓRICO DE ALTERAÇÕES
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 | [nome do autor] | Criação do template de descrição do dataset
2026-09-24 | [nome do autor] | Download dos dados reais do IBGE/SIDRA (Tabela 1612) e do ONI/NOAA; documentação atualizada
-->

# Dataset — descrição

## Fontes

| Fonte | Conteúdo | Período | Granularidade | Link | Status |
|---|---|---|---|---|---|
| IBGE/SIDRA — Tabela 1612 | Área plantada, área colhida, produção e rendimento médio de soja | 2000–2023 | Município (RS) | https://sidra.ibge.gov.br/tabela/1612 | ✅ baixado — `dataset/raw/ibge_sidra_1612_soja_rs_2000_2023.csv` |
| NOAA/CPC — ONI | Índice trimestral (médias móveis de 3 meses) do ENOS (El Niño/La Niña) | 1999–2024 | Trimestral (a agregar por safra) | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt | ✅ baixado — `dataset/raw/noaa_oni_1999_2024.csv` |
| INMET — BDMEP | Precipitação e temperatura observadas | 2000–2023 | Estação meteorológica | https://bdmep.inmet.gov.br/ | ❌ **pendente** — API do INMET (`apitempo.inmet.gov.br`, `bdmep.inmet.gov.br`) não respondeu nas tentativas automatizadas; requer download manual via portal BDMEP (cadastro + token gratuito) |
| Embrapa / CQFS-RS/SC | Recomendações de adubação fosfatada (MAP, Superfosfato Simples, Superfosfato Triplo, DAP) | — | Classe de solo/região | (referência bibliográfica, sem API — dados a transcrever do manual) | ❌ pendente — transcrever manualmente do manual CQFS-RS/SC (2016) |

### Como os dados do IBGE foram obtidos

Via API pública do SIDRA (sem necessidade de token), tabela 1612, variáveis
109 (área plantada), 216 (área colhida), 214 (quantidade produzida) e 112
(rendimento médio), classificação 81 categoria 2713 (Soja em grão), para
todos os municípios do RS (`N6[N3[43]]`), período 2000–2023:

```
https://servicodados.ibge.gov.br/api/v3/agregados/1612/periodos/2000-2023/variaveis/109|216|214|112?localidades=N6[N3[43]]&classificacao=81[2713]
```

O JSON bruto está em `dataset/raw/ibge_sidra_1612_soja_rs_2000_2023_raw.json`
e a versão já tabulada (município × ano, uma linha por combinação) em
`dataset/raw/ibge_sidra_1612_soja_rs_2000_2023.csv` (11.928 linhas = 497
municípios × 24 safras). Valores ausentes (município sem produção de soja
naquele ano) aparecem como célula vazia.

### Como os dados do ONI foram obtidos

Arquivo ASCII oficial da NOAA/CPC (sem necessidade de API key):

```
https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt
```

Cada linha é uma janela móvel de 3 meses (ex.: `DJF` = dez–jan–fev).
`dataset/raw/noaa_oni_1999_2024.csv` traz a série filtrada para 1999–2024
com colunas `seas`, `ano`, `total_sst`, `oni_anom` (o `oni_anom` é o índice
ONI propriamente dito). **Ainda falta**, no notebook de preparação, agregar
essas janelas trimestrais para uma métrica por safra (ex.: média do ONI nas
janelas que cobrem a semeadura–colheita de cada safra no RS, tipicamente
out–mar).

## Chaves e formato final

- Chave primária da base final (a ser gerada no notebook): `codigo_ibge_municipio` + `ano_safra`
- Arquivo(s) brutos (já disponíveis): `dataset/raw/`
- Arquivo(s) processado(s)/final(is) (a gerar nos notebooks): `dataset/processed/painel_municipio_safra.csv`

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
| `precipitacao_mm` | Precipitação observada (estação mais próxima) | mm | INMET |
| `temperatura_media_c` | Temperatura média observada | °C | INMET |
| `dose_p2o5_recomendada` | Dose de P₂O₅ recomendada por classe de solo | kg/ha | Embrapa / CQFS-RS/SC |
| ... | [completar conforme colunas finais geradas nos notebooks] | | |

## Limitações conhecidas

- Dados de adubação são **recomendações agronômicas por classe de solo**, não
  consumo real por produtor/município/ano.
- Municípios criados por desmembramento ao longo do período (2000–2023)
  podem ter séries históricas incompletas.
- A estação INMET usada por município é a mais próxima disponível, podendo
  não representar exatamente o microclima local.

## Licença de uso dos dados originais

Todas as fontes são públicas (governamentais/institucionais). Citar a fonte
original ao reutilizar os dados.
