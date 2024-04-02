---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.4
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---
```{code-cell} ipython3
:tags: ["remove-cell"]

from datetime import datetime
from myst_nb import glue

today = datetime.today().strftime("%d.%m.%Y")
glue("today", today)
```

# Überblick
Dies ist das Skript für die Vorlesung Optimierung, Modellierung und Simulation an der Hochschule Karlsruhe im Studiengang Data Science. Letze Änderung am {glue:text}`today`.

## Inhaltsverzeichnis
Die Vorlesung ist in zwei Teile gegliedert, die im Prinzip unabhängig voneinander gelesen werden können. 

Im Teil "Lineare Optimierungsmodelle" liegt der Fokus auf Problemmodellierung von Planungs- und Entscheidungsprobleme als gemischt-ganzzahlige lineare Optimierungsprobleme. Die Inhalte werden oft dem *Operations Research* zugerechnet.

Im Teil "Ableitungsbasierte Optimierung" werden gradientenbasierte Optimierungsverfahren behandelt, wie sie z.B. beim Training von Modellen des maschinellen Lernens benutzt werden. Dabei werden auch die benötigten Grundbegriffe der multivariaten Analysis eingeführt.


```{tableofcontents}
```

## Literatur

Teil 1:
- R. Bauer: Skript *Datenbasierte Optimierung in der Unternehmenspraxis*, Hochschule Karlsruhe 2021.
- N. Sudermann-Merx: *Einführung in Optimierungsmodelle*, Springer, 2023
- H. P. Williams: *Model Building in Mathematical Programming, 5th Edition*, Wiley, 2013.
- [Gurobi Resource Center](https://www.gurobi.com/resource-center/?post_types=jupyter_models)

Teil 2:
- M. P. Deisenroth, A. A. Faisal, C. S. Ong: *Mathematics for Machine Learning*, Springer, 2021
- J. Watt, R. Borhani, A. Katsaggelos: *Machine learning refined: foundations, algorithms, and applications, 2nd edition*, Cambridge University Press 2020
- M. J. Kochenderfer, T. A. Wheeler: *Algorithms for Optimization*, The MIT Press, 2019
- J. Nocedal, S. J. Wright: *Numerical Optimization*, Springer, 2006

## Kontakt
Wenn Sie Fehler finden oder sonstige Kommentare und Anregungen haben, schreiben Sie mir gerne eine E-Mail: dennis.janka@h-ka.de.