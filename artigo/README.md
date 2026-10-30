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
2026-10-30 |                 | Word volta ao padrão visual da versão anterior (sem capa nem sumário) e com o título antigo; mantidos os tópicos novos
2026-10-30 |                 | `.tex` reorganizado com os mesmos tópicos e texto do Word; nova figura `fig7_previsao_2026_perspectiva_2027.png`
-->

# Artigo

O artigo existe em duas versões com o mesmo conteúdo e os mesmos tópicos
(resumo executivo, introdução, dados, metodologia, etapas 1–6, modelo
final, previsão 2026, perspectiva 2027, discussão, conclusões e apêndices
de adubação e reprodutibilidade). Ao mudar um texto ou um número, atualize
as duas.

- `latex/artigo-grupo.tex` — versão no template da SBC (mais os arquivos
  de estilo `sbc-template.sty` e `caption2.sty`, necessários para
  compilar). Tem também o resumo/abstract exigidos pelo template.
- `latex/figuras/` — figuras do artigo. Usadas no `.tex`:
  `fig2_rendimento_por_enos.png` (Figura 1, de
  `notebooks/analise_exploratoria.ipynb`); `fig4` a `fig6` (Figuras 2 a 4,
  modelo FL com o NASA POWER, de
  `notebooks/modelagem_etapa5_nasa_power.ipynb`); e
  `fig7_previsao_2026_perspectiva_2027.png` (Figura 5, previsão 2026 e
  cenários 2027, extraída do Word). `fig1` e `fig3` são da análise
  exploratória e não entram mais no texto.
- `word/Relatorio_N1_Soja_RS.docx` — versão Word do artigo.
- `artigo-grupo.pdf` — **[adicionar aqui]** o PDF final, após compilar o
  `.tex` (ex.: via Overleaf) e após a revisão do grupo.

## Como compilar

1. Suba os três arquivos de `latex/` e a pasta `latex/figuras/` para um
   projeto novo no Overleaf (ou compile localmente com `pdflatex`, se tiver
   LaTeX instalado; as referências estão no próprio `.tex`).
2. Gere o PDF e salve-o nesta pasta como `artigo-grupo.pdf`.
3. Confira se o PDF está de acordo com o template SBC (margens, fontes,
   limite de páginas) antes da entrega final no AVA.
