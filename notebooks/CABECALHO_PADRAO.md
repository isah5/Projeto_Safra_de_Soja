# Cabeçalho padrão para os arquivos-fonte

O enunciado exige que **todos os arquivos-fonte** (notebooks `.ipynb`,
scripts `.py`, e opcionalmente `.tex`/`.md`) tragam, no topo, identificação
do grupo e histórico de alterações. Use um dos modelos abaixo.

O enunciado pede, especificamente, três blocos: (1) identificação completa
dos membros do grupo, (2) **síntese do conteúdo do arquivo** e (3) histórico
de alterações (data, autor, descrição). Os modelos abaixo já trazem os três.

## Para notebooks (.ipynb) — primeira célula, tipo Markdown

```markdown
# Previsão de Produtividade Municipal da Soja no RS — Análise Exploratória

**Grupo:** [preencher]
**Integrantes:** Isabelle Franco (RA 10425395) · Gustavo Rodrigues (RA 10403091) ·
Pedro Henrique (RA 10388298) · Lorenzo Tadeo (RA 10420067)
**Orientador:** Prof. Dr. Ivan Carlos Alcântara de Oliveira

**Síntese do conteúdo deste arquivo:** [preencher — ex.: "Carrega os dados
brutos do IBGE/SIDRA, ONI e INMET, realiza a limpeza e integração em nível
município–safra, e apresenta a análise exploratória (distribuições,
correlações, cobertura temporal/espacial e relação ONI × rendimento)."]

| Data       | Autor           | Descrição                              |
|------------|-----------------|-----------------------------------------|
| 2026-09-24 | [nome do autor] | Criação do notebook / primeira versão   |
```

## Para scripts Python (.py) — primeiras linhas, como comentário

```python
"""
Previsão de Produtividade Municipal da Soja no RS
Integrantes: Isabelle Franco (RA 10425395), Gustavo Rodrigues (RA 10403091),
             Pedro Henrique (RA 10388298), Lorenzo Tadeo (RA 10420067)
Orientador: Prof. Dr. Ivan Carlos Alcântara de Oliveira

Síntese do conteúdo deste arquivo: [preencher — o que este script faz]

Histórico de alterações:
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 | [nome do autor] | Criação inicial do script
"""
```

## Regra prática

- Toda vez que um integrante alterar um arquivo de forma relevante, ele
  **acrescenta uma nova linha** na tabela de histórico (não apaga as
  anteriores) com data, seu nome e uma descrição curta da mudança.
- O mesmo cabeçalho (adaptado para comentário `%` em vez de `"""`) deve
  entrar no início do `.tex` do artigo — ver `artigo-grupo.tex`.
