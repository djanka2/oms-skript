---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Quadratische Probleme
## Beispiele
## Anwendung: Training von linearen Regressionsmodellen

## Grundlagen der beschränkten Optimierung


### Gleichungsbeschränkte Optimierung

### Ungleichungsbeschränkte Optimierung
````{prf:example} Aufstellen der KKT-Bedingungen
:label: example:KKT

Gegeben sei das Optimierungsproblem

\begin{align*}
\min_{x,y \in \mathbb{R}} \quad & \frac{1}{2}(x-2)^2+\frac{1}{2}(y-\frac{1}{2})^2 \\
\text{s.t.} \quad & (x+1)^{-1}-y-\frac{1}{4}\geq 0\\
& x\geq 0\\
& y\geq 0
\end{align*}

Wir stellen dafür nun die KKT-Bedingungen auf. Dazu benötigen wir die Lagrange-Funktion, bei der wir für jede Nebenbedingung einen Lagrange-Multiplikator $\mu_i$ einführen:

\begin{align*}
\mathcal{L}(x,y,\mu_1,\mu_2,\mu_3) = \frac{1}{2}(x-2)^2+\frac{1}{2}(y-\frac{1}{2})^2 - \mu_1\left((x+1)^{-1}-y-\frac{1}{4}\right) - \mu_2 x - \mu_3 y
\end{align*}

Nun können wir die KKT-Bedingungen aufstellen. Dies sind die folgenden Gruppen von Gleichungen bzw. Ungleichungen (insgesamt 5 Gleichungen und 6 Ungleichungen):

1. Der Gradient der Lagrange-Funktion nach $x$ und $y$ muss $0$ sein (Stationarität):  
    \begin{align*}
    \frac{\partial \mathcal{L}}{\partial x} &= x-2 + \frac{\mu_1}{(x+1)^2} - \mu_2 = 0\\
    \frac{\partial \mathcal{L}}{\partial y} &= y-\frac{1}{2} + \mu_1 - \mu_3 = 0
    \end{align*}
2. Die Nebenbedingungen müssen erfüllt sein (Zulässigkeit):  
    \begin{align*}
    (x+1)^{-1}-y-\frac{1}{4}&\geq 0\\
    x&\geq 0\\
    y&\geq 0
    \end{align*}  
3. Die Lagrange-Multiplikatoren müssen nicht-negativ sein (Nicht-Negativität):  
    \begin{align*}
    \mu_1 &\geq 0\\
    \mu_2 &\geq 0\\
    \mu_3 &\geq 0
    \end{align*}  
4. Entweder muss die Ungleichungsnebenbedingung gleich $0$ sein oder der zugehörige Lagrange-Multiplikator (Komplementarität):  
    \begin{align*}
    \mu_1\left((x+1)^{-1}-y-\frac{1}{4}\right) &= 0\\
    \mu_2 x &= 0\\
    \mu_3 y &= 0
    \end{align*}

Die Schwierigkeit, einen KKT-Punkt (also einen Punkt, der alle Bedingungen erfüllt) zu finden, liegt darin, dass wir es mit einem System aus Gleichungen und *Ungleichungen* zu tun haben. Wir können nicht einfach die Gleichungen nach $x, y$ und $\mu_1,\mu_2,\mu_3$ auflösen. Stattdessen müssen wir Fallunterscheidungen machen, je nachdem, ob die Ungleichungsnebenbedingungen aktiv sind (d.h. es gilt $=$) oder nicht (d.h. es gilt $>$).

Praktisch müsste man alle $2^3$ Möglichkeiten durchgehen, welche der drei Ungleichungsnebenbedingungen mit Gleichheit erfüllt sind, also *aktiv* sind. Bei den Ungleichungen, die $>0$ sind (die *inaktiven* Ungleichungsnebenbedingungen) muss der zugehörige Lagrange-Multiplikator $0$ sein, damit Komplementarität erfüllt ist. 

Für die aktiven Ungleichungen muss man nun testweise ein Gleichungssystem lösen. Nach der Lösung muss man das Vorzeichen der $\mu_1,\mu_2,\mu_3$ überprüfen: Nur wenn diese nicht negativ sind, ist die Nicht-Negativitätsbedingung der KKT-Bedingungen erfüllt und der so berechnete Punkt ist ein KKT-Punkt. Ist das nicht der Fall, muss eine andere Kombination von aktiven Ungleichungsnebenbedingungen getestet werden.
````



%## Anwendung: Support Vector Maschinen