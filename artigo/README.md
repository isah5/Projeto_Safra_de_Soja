<!--
Grupo:
Orientador:

HISTÓRICO DE ALTERAÇÕES
Data       | Autor           | Descrição
-----------|-----------------|--------------------------------------------
2026-09-24 |                 | Criação da pasta do artigo + fonte LaTeX inicial
2026-10-23 |                 | Inclusão da pasta de figuras e da versão Word na descrição
2026-10-30 |                 | `.tex` e Word atualizados com as Etapas 5 e 6 (NASA POWER, modelo FL, previsão 2026 e perspectiva 2027) e com as figuras regeradas
2026-10-30 |                 | Word reestruturado como relatório da previsão 2026 e da perspectiva 2027; números conferidos com as saídas dos notebooks
-->

# Artigo

- `latex/artigo-grupo.tex` — fonte do artigo no template da SBC (mais os
  arquivos de estilo `sbc-template.sty` e `caption2.sty`, necessários para
  compilar).
- `latex/figuras/` — Figuras 1 a 6 do artigo: 1 a 3 geradas por
  `notebooks/analise_exploratoria.ipynb` e 4 a 6 (modelo final FL com o
  NASA POWER) por `notebooks/modelagem_etapa5_nasa_power.ipynb`.
- `word/Relatorio_N1_Soja_RS.docx` — relatório técnico das etapas de
  modelagem, da previsão da safra 2026 e da perspectiva da safra 2027.
  Usa os mesmos resultados do `.tex`, mas com outra estrutura (resumo
  executivo, calendário das safras, etapas 1–6, adubação em apêndice);
  ao mudar um número, atualize os dois.
- `artigo-grupo.pdf` — **[adicionar aqui]** o PDF final, após compilar o
  `.tex` (ex.: via Overleaf) e após a revisão do grupo.

## Como compilar

1. Suba os três arquivos de `latex/` e a pasta `latex/figuras/` para um
   projeto novo no Overleaf (ou compile localmente com `pdflatex`, se tiver
   LaTeX instalado; as referências estão no próprio `.tex`).
2. Gere o PDF e salve-o nesta pasta como `artigo-grupo.pdf`.
3. Confira se o PDF está de acordo com o template SBC (margens, fontes,
   limite de páginas) antes da entrega final no AVA.
