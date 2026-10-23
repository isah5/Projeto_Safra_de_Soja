# Previsão de Produtividade Municipal da Soja no Rio Grande do Sul com Aprendizado de Máquina e Variáveis Agrometeorológicas

<!--
CABEÇALHO DE IDENTIFICAÇÃO DO GRUPO
Grupo:
Integrantes:
Prof:
Disciplina: Inteligência Artificial
Instituição: Universidade Presbiteriana Mackenzie - FCI

HISTÓRICO DE ALTERAÇÕES
Data       | Autor              | Descrição
-----------|--------------------|--------------------------------------------
2026-09-24 |                    | Criação inicial do repositório (estrutura N1)
2026-10-23 |                    | Descrição dos notebooks de modelagem (Etapas 1-4), do modelo final e da ordem de execução
-->

Repositório público do projeto da disciplina, com o artigo científico
(template SBC), o dataset utilizado e os notebooks Python de análise
exploratória e de modelagem.

## Estrutura do repositório

```
.
├── artigo/         # Artigo (template SBC): fonte LaTeX, figuras e versão Word
├── dataset/        # Dados brutos e processados + descrição (dataset/README.md)
├── notebooks/      # Notebooks Python: análise exploratória e modelagem (Etapas 1-4)
└── README.md
```

## Notebooks

A modelagem foi feita em quatro etapas, cada uma motivada pelo diagnóstico
dos erros da anterior:

| Notebook | Conteúdo | Principal resultado |
|---|---|---|
| `analise_exploratoria.ipynb` | Integração das fontes e painel município–safra | `dataset/processed/painel_municipio_safra.csv` |
| `modelagem.ipynb` (Etapa 1) | Baseline, Regressão Linear, Random Forest e Gradient Boosting com clima agregado (out–mar) | R² negativo no teste 2021–2025: o total de chuva não distingue as safras |
| `modelagem_etapa2.ipynb` (Etapa 2) | Clima por subperíodo do ciclo (out–nov, dez–fev, mar) a partir do INMET diário | O clima passa a explicar as safras, mas a tendência extrapolada enviesa 2021–2025 |
| `modelagem_etapa3.ipynb` (Etapa 3) | Patamar calculado só com safras anteriores (média móvel de 5 anos) + regressão linear reduzida | RMSE 767 / 689 kg/ha; supera as linhas de base; contribuição dos fatores e erro por região |
| `modelagem_etapa4.ipynb` (Etapa 4) | Balanço hídrico (Hargreaves–Samani + balde), limiares de seca extrema e recomendação de adubação | **Modelo final (H2):** RMSE 740 / 684 kg/ha, R² 0,31 / 0,26 |

RMSE e R² são dados como "corte temporal (teste 2021–2025) / deixando uma
safra de fora". O modelo final reduz o RMSE em 14% e 22% em relação à média
histórica do município. Detalhes em [`artigo/`](artigo/).

## Como reproduzir

1. Clone o repositório: `git clone https://github.com/isah5/Projeto_Safra_de_Soja`
2. Instale as dependências: `pip install -r notebooks/requirements.txt`
3. Os dados brutos e o dicionário de variáveis estão descritos em
   [`dataset/README.md`](dataset/README.md).
4. Execute os notebooks a partir da pasta [`notebooks/`](notebooks/), nesta
   ordem: `analise_exploratoria`, `modelagem`, `modelagem_etapa2`,
   `modelagem_etapa3` e `modelagem_etapa4`. A Etapa 2 gera
   `dataset/processed/clima_subperiodos_estacao_safra.csv`, usado pelas
   Etapas 3 e 4; a Etapa 4 gera
   `dataset/processed/recomendacao_adubacao_safra2026.csv`.

## Artigo

A fonte LaTeX, as figuras e a versão Word do artigo estão em
[`artigo/`](artigo/).

## Licença / Uso dos dados

Este projeto utiliza exclusivamente dados públicos (IBGE/SIDRA, NOAA, INMET,
Embrapa/CQFS-RS-SC), agregados em nível municipal, sem dados pessoais.
