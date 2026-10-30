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
2026-10-30 |                 | Artigo migrado do template SBC para o template de TCC da FCI (abnTeX2 e Word), com referencial teórico, hipótese e citações ABNT
-->

# Artigo

O artigo segue o template de TCC da FCI/Mackenzie (2026) e existe em duas
versões com o mesmo conteúdo: resumo e abstract, introdução, referencial
teórico, metodologia, resultados e discussão, conclusão e referências (ABNT).
Ao mudar um texto ou um número, atualize as duas. O template exige resumo
de 150 a 250 palavras e no máximo 20 páginas, incluindo as referências.

- `Latex/Artigo_TCC_Soja_RS.tex` — versão LaTeX (classe abnTeX2), com as
  referências em `Latex/referencias.bib` e o logotipo do cabeçalho em
  `Latex/FCI.png`.
- `Latex/figuras/` — figuras do artigo: `fig2_rendimento_por_enos.png`
  (Figura 1, de `notebooks/analise_exploratoria.ipynb`); `fig4` a `fig6`
  (Figuras 2 a 4, modelo FL com o NASA POWER, de
  `notebooks/modelagem_etapa5_nasa_power.ipynb`); e
  `fig7_previsao_2026_perspectiva_2027.png` (Figura 5, previsão 2026 e
  cenários 2027, de `notebooks/modelagem_etapa6_previsao_2026_2027.ipynb`).
- `Word/Artigo_TCC_Soja_RS.docx` — versão Word do artigo.
- `Latex/TemplateArtigoTCC_2026.tex`, `Latex/TemplateArtigoTCC_2026.pdf`,
  `Word/TemplateArtigo_TCC_FCI_2026.doc` e `.pdf` — templates originais da
  FCI, mantidos como referência.

## Como compilar

1. Suba `Artigo_TCC_Soja_RS.tex`, `referencias.bib`, `FCI.png` e a pasta
   `figuras/` para um projeto novo no Overleaf (compilador pdfLaTeX) ou
   compile localmente com `pdflatex` → `bibtex` → `pdflatex` → `pdflatex`.
2. Gere o PDF e salve-o nesta pasta como `Artigo_TCC_Soja_RS.pdf`.
3. Preencha os nomes do grupo e do orientador e confira o limite de 20
   páginas antes da entrega final.
