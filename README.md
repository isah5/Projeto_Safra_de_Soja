# Modelagem preditiva da produtividade da safra de soja com uso de aprendizado de máquina e dados agrometeorológicos

<!--
CABEÇALHO DE IDENTIFICAÇÃO DO GRUPO
Disciplina: Inteligência Artificial
Instituição: Universidade Presbiteriana Mackenzie - FCI

HISTÓRICO DE ALTERAÇÕES
Data       | Descrição
-----------|--------------------------------------------
2026-09-24 | Criação inicial do repositório (estrutura N1)
2026-10-23 | Descrição dos notebooks de modelagem (Etapas 1-4), do modelo final e da ordem de execução
2026-10-23 | Etapa 5 (clima do NASA POWER) e script de download
2026-10-26 | Junção com a main: Etapas 3-4 com patamar até Y−2; Etapa 5 ajustada à mesma regra (resultados a regerar)
2026-10-29 | Etapa 6: previsão da safra 2026 e perspectiva da safra 2027
2026-10-30 | Ambiente padrão (.venv, Python 3.13) e instruções de execução dos notebooks
2026-10-30 | Resultados da Etapa 5 atualizados após a reexecução com o patamar até Y−2
2026-10-30 | Artigo no template de TCC da FCI (abnTeX2 e Word)
-->

Repositório público do projeto da disciplina, com o artigo científico
(template de TCC da FCI), o dataset utilizado e os notebooks Python de análise
exploratória e de modelagem.

## Estrutura do repositório

```
.
├── artigo/         # Artigo (template de TCC da FCI): fonte LaTeX, figuras e versão Word
├── dataset/        # Dados brutos e processados + descrição (dataset/README.md)
├── notebooks/      # Notebooks Python: análise exploratória e modelagem (Etapas 1-6)
└── README.md
```

## Notebooks

A modelagem foi feita em cinco etapas, cada uma motivada pelo diagnóstico
dos erros da anterior, e a sexta aplica o modelo final à próxima safra:

| Notebook | Conteúdo | Principal resultado |
|---|---|---|
| `analise_exploratoria.ipynb` | Integração das fontes e painel município–safra | `dataset/processed/painel_municipio_safra.csv` |
| `modelagem.ipynb` (Etapa 1) | Baseline, Regressão Linear, Random Forest e Gradient Boosting com clima agregado (out–mar) | R² negativo no teste 2021–2025: o total de chuva não distingue as safras |
| `modelagem_etapa2.ipynb` (Etapa 2) | Clima por subperíodo do ciclo (out–nov, dez–fev, mar) a partir do INMET diário | O clima passa a explicar as safras, mas a tendência extrapolada enviesa 2021–2025 |
| `modelagem_etapa3.ipynb` (Etapa 3) | Patamar calculado só com as safras já publicadas na data da previsão (média móvel de 5 safras; para prever 2026, 2020–2024) + regressão linear reduzida | RMSE 873 / 714 kg/ha; supera as linhas de base na validação deixando uma safra de fora; contribuição dos fatores e erro por região |
| `modelagem_etapa4.ipynb` (Etapa 4) | Balanço hídrico (Hargreaves–Samani + balde), limiares de seca extrema e recomendação de adubação | **Modelo final até a Etapa 4 (H2):** RMSE 870 / 706 kg/ha, R² 0,05 / 0,21; custo da defasagem de publicação (para prever 2026: patamar 2020–2024, publicado, × 2021–2025, hipotético) |
| `modelagem_etapa5_nasa_power.ipynb` (Etapa 5) | Clima do NASA POWER (grade, sem falhas) no lugar do INMET: comparação entre as fontes, modelos F, H2 e Gradient Boosting e combinações de F e H2 | Cobertura de ~5,2 mil para ~8,3 mil pares município–safra (+58%) e erro menor que o do INMET nas mesmas linhas. **Novo modelo final (FL = F + limiar de déficit):** RMSE 772 / 626 kg/ha, R² 0,28 / 0,40 |
| `modelagem_etapa6_previsao_2026_2027.ipynb` (Etapa 6) | Validação dos cinco modelos com o patamar só das safras publicadas, previsão da safra 2026 por município (comparada ao LSPA/IBGE) e perspectiva da safra 2027 por cenários climáticos (El Niño) | **FL reconfirmado:** RMSE 772 / 626 kg/ha. Safra 2026: FL prevê 2.097 kg/ha, contra 2.734 kg/ha do LSPA (subestima ~23%). Safra 2027: mediana de 2.831 kg/ha nos cenários de El Niño |

RMSE e R² são dados como "corte temporal (teste 2021–2025) / deixando uma
safra de fora". A previsão de cada safra é emitida em 31 de março do ano da
colheita e usa só dados publicados até essa data. Como o IBGE divulga o rendimento
municipal (PAM) em setembro do ano seguinte à colheita:

| Safra prevista | Emissão da previsão | Última PAM publicada | Patamar (5 safras) |
|---|---|---|---|
| 2026 | 31/03/2026 | 2024 (set/2025) | 2020–2024 |
| 2027 | 31/03/2027 | 2025 (set/2026) | 2021–2025 |

Na validação histórica vale a mesma regra: a safra 2022, por exemplo, é prevista
em 31/03/2022 com o patamar 2016–2020. Nessas condições, o modelo H2 reduz o RMSE
em 22% em relação à média histórica do município na validação deixando uma safra
de fora e empata com ela no corte 2021–2025, período de secas consecutivas.
Detalhes em [`artigo/`](artigo/).

## Como reproduzir

Todos os notebooks e o script devem rodar no mesmo ambiente: o `.venv` do
projeto, com **Python 3.13** e as versões fixadas em
[`notebooks/requirements.txt`](notebooks/requirements.txt). Versões diferentes
mudam levemente os resultados.

1. Clone o repositório: `git clone https://github.com/isah5/Projeto_Safra_de_Soja`
2. Crie o ambiente uma única vez, a partir da raiz do repositório, com o
   [`uv`](https://docs.astral.sh/uv/):
   `uv venv --python 3.13` e `uv pip install -r notebooks/requirements.txt ipykernel nbconvert`.
3. Os dados brutos e o dicionário de variáveis estão descritos em
   [`dataset/README.md`](dataset/README.md).
4. Execute os notebooks no kernel do `.venv` — no VS Code, *Select Kernel* →
   *Python Environments* → `.venv (Python 3.13)`; depois *Run All*. Pelo
   terminal, a partir de [`notebooks/`](notebooks/):
   `..\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace <notebook>.ipynb`.
   Ordem: `analise_exploratoria`, `modelagem`, `modelagem_etapa2`,
   `modelagem_etapa3`, `modelagem_etapa4`, `modelagem_etapa5_nasa_power` e
   `modelagem_etapa6_previsao_2026_2027`. A
   Etapa 2 gera `dataset/processed/clima_subperiodos_estacao_safra.csv`, usado
   pelas Etapas 3 a 5; a Etapa 4 gera
   `dataset/processed/recomendacao_adubacao_safra2026.csv` e
   `dataset/processed/balanco_hidrico_estacao_safra.csv` (usado pela Etapa 5).
   Os dados do NASA POWER já estão em `dataset/raw/`; para baixá-los de novo,
   rode `.venv\Scripts\python.exe dataset/baixar_nasa_power.py` a partir da raiz do repositório
   (e `.venv\Scripts\python.exe dataset/baixar_nasa_power.py 20260101 20260531 nasa_power_rs_2026.csv`
   para o complemento da safra 2026, usado pela Etapa 6).

## Artigo

A fonte LaTeX, as figuras e a versão Word do artigo estão em
[`artigo/`](artigo/).

## Licença / Uso dos dados

Este projeto utiliza exclusivamente dados públicos (IBGE/SIDRA, NOAA, INMET,
NASA POWER, Embrapa/CQFS-RS-SC), agregados em nível municipal, sem dados pessoais.
