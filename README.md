# Previsão de Produtividade Municipal da Soja no Rio Grande do Sul com Aprendizado de Máquina e Variáveis Agrometeorológicas

<!--
CABEÇALHO DE IDENTIFICAÇÃO DO GRUPO
Grupo: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
       Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067)
Integrantes: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
             Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067)
Prof: Dr. Ivan Carlos Alcântara de Oliveira
Disciplina: Inteligência Artificial
Instituição: Universidade Presbiteriana Mackenzie - FCI

HISTÓRICO DE ALTERAÇÕES
Data       | Autor              | Descrição
-----------|--------------------|--------------------------------------------
2026-09-24 | Isabelle Franco    | Criação inicial do repositório (estrutura N1)
-->

Repositório público do projeto da disciplina, com o artigo científico
(template SBC), o dataset utilizado e os notebooks de análise exploratória
em Python.

## Estrutura do repositório

```
.
├── artigo/         # PDF final do artigo (template SBC) e fonte (.tex/.docx)
├── dataset/        # Dados utilizados + descrição (dataset/README.md)
├── notebooks/       # Notebook(s) Python da análise exploratória
└── README.md
```

## Como reproduzir

1. Clone o repositório: `git clone <url-do-repositorio>`
2. Instale as dependências (ver `notebooks/requirements.txt`, se aplicável).
3. Os dados brutos e o dicionário de variáveis estão descritos em
   [`dataset/README.md`](dataset/README.md).
4. A análise exploratória está em [`notebooks/`](notebooks/).

## Artigo

O artigo final (PDF) está em [`artigo/`](artigo/).

## Licença / Uso dos dados

Este projeto utiliza exclusivamente dados públicos (IBGE/SIDRA, NOAA, INMET,
Embrapa/CQFS-RS-SC), agregados em nível municipal, sem dados pessoais.
