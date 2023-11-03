watch-latex:
  latexmk -pdf -quiet -pdflatex="pdflatex -synctex=1 -interaction=nonstopmode" -pvc -bibtex cards.tex

watch-input:
  ls *.py *.toml | entr python cards.py
