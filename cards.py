import itertools
import textwrap
import toml

NROWS = 3
NCOLS = 3


TEMPLATE=r"""
\documentclass[a4paper,12pt]{article}

\usepackage[utf8]{inputenc}
\usepackage[margin=1cm,inner=0.4cm,outer=0.4cm]{geometry}
\usepackage{tcolorbox}
\usepackage{listings}

\pagestyle{empty}

\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{1,1,1}
\lstdefinestyle{mystyle}{
    backgroundcolor=\color{backcolour},
    commentstyle=\color{codegreen},
    keywordstyle=\color{magenta},
    numberstyle=\tiny\color{codegray},
    stringstyle=\color{codepurple},
    basicstyle=\ttfamily\footnotesize,
    breakatwhitespace=false,
    breaklines=true,
    captionpos=b,
    keepspaces=true,
    showspaces=false,
    showstringspaces=false,
    showtabs=false,
    tabsize=2
}
\lstset{language=Python, style=mystyle}

\newtcolorbox{fcardfront}[1]{
  title=#1,
  after=\hfill,
  valign=center,
  width=0.3333\textwidth,
  height=0.3\textheight
}

\begin{document}

\tcbset{width=0.3\textwidth, height=0.3\textheight, before=, after=\hfill, colback=white, valign=center}

%s

\end{document}
"""


def batched(iterable, n):
    batches = []
    batch = []
    for elem in iterable:
        batch.append(elem)
        if len(batch) >= n:
            batches.append(tuple(batch))
            # yield tuple(batch)
            batch = []
    # return tuple(batch)
    if len(batch) != 0:
        while len(batch) < n:
            batch.append(None)
        batches.append(tuple(batch))
    return batches
    

def empty():
    s = """
    \\begin{tcolorbox}
    \\end{tcolorbox}"""
    return textwrap.dedent(s)


def front(text, title, version):
    s = """
    \\begin{tcolorbox}[title=%s, text fill]
        \\par\\vfill
        %s
        \\par\\vfill
        \\begin{flushright}
        \\tiny{versione: %s}
        \\end{flushright}
    \\end{tcolorbox}""" % (title, text, version)
    return textwrap.dedent(s)

def back(text, title):
    s = """
    \\begin{tcolorbox}[title=%s, colbacktitle=black!10, coltitle=black, left=1mm, right=1mm]
        \\begin{lstlisting}
%s\\end{lstlisting}
    \\end{tcolorbox}""" % (title, text)
    return textwrap.dedent(s)

def build_page(cards, version):
    # Build front
    rows = []
    for row in batched(cards, NROWS):
        row_str = "".join([
            front(card['front'], card['title'], version) if card is not None else empty()
            for card in row
        ])
        rows.append(row_str)
    page_front = "\n\n\\vfill\n".join(rows)

    rows = []
    for row in batched(cards, NROWS):
        row_str = "".join([
            back(card['back'], card['title']) if card is not None else empty()
            for card in reversed(row)
        ])
        rows.append(row_str)
    page_back = "\n\n\\vfill\n".join(rows)

    return page_front + "\n" + page_back

def build_pages(cards, version):
    pages = []
    for page_cards in batched(cards, NROWS * NCOLS):
        page = build_page(page_cards, version)
        pages.append(page)
    assert len(pages) > 0
    pages = "\n".join(pages)
    return TEMPLATE % pages


def main(infile, outfile):
    with open(infile) as fp:
        cards = toml.load(fp)
        version = cards['version']
        cards = cards['cards']
    pages = build_pages(cards, version)
    with open(outfile, "w") as fh:
        print(pages, file=fh)

main("cards.toml", "cards.tex")

