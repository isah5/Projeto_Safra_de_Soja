<!--
Grupo: [preencher] | Integrantes: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067) | Orientador: Prof. Dr. Ivan Carlos Alcântara de Oliveira

HISTÓRICO DE ALTERAÇÕES
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 | [nome do autor] | Criação do template de descrição do dataset
-->

# Dataset — descrição

Breve descrição do dataset usado no projeto, conforme exigido pelo enunciado.

## Fontes

| Fonte | Conteúdo | Período | Granularidade | Link |
|---|---|---|---|---|
| IBGE/SIDRA — Tabela 1612 | Rendimento (kg/ha), área plantada/colhida e produção de soja | 2000–2023 | Município (RS) | https://sidra.ibge.gov.br/tabela/1612 |
| NOAA/CPC — ONI | Índice trimestral do ENOS (El Niño/La Niña) | 2000–2023 | Trimestral (agregado por safra) | https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php |
| INMET — BDMEP | Precipitação e temperatura observadas | 2000–2023 | Estação meteorológica | https://bdmep.inmet.gov.br/ |
| Embrapa / CQFS-RS/SC | Recomendações de adubação fosfatada (MAP, SS, ST, DAP) | — | Classe de solo/região | (referência bibliográfica, sem link direto de dados) |

## Chaves e formato final

- Chave primária: `codigo_ibge_municipio` + `ano_safra`
- Arquivo(s): [preencher nome dos arquivos .csv/.parquet gerados, ex.: `dataset/processed/painel_municipio_safra.csv`]

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
