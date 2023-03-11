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

(sec:gradientenverfahren)=
# Gradientenverfahren
In diesem Abschnitt schauen wir uns Details zu Gradientenverfahren an. Wir wollen das weiterhin anhand von einfachen, niedrig-dimensionalen (1d und 2d) Beispielen tun, um die Konzepte und Probleme der Verfahren zu verstehen. 

Behalten Sie aber im Hinterkopf, dass die eigentliche Motivation von aktuellen Gradientenverfahren die Lösung von sehr schwierigen, hochdimensionalen Problemen ist. Gradientenverfahren werden z.B. dazu eingesetzt moderne KI-Systeme mit vielen Millionen bzw. Milliarden von Variablen zu trainieren.

Das big picture: Wir sind nach wie vor an Optimierungsproblemen der Form
\ba  
\min_{\v x\in\R^n} f(\v x)
\ea 
interessiert. Wir begnügen uns dabei mit *lokalen* Lösungen (von denen wir für streng konvexe Funktionen immerhin wissen, dass sie auch global sind). 

````{note}
Die Aufgabe, globale Minima für allgemeine, nicht-konvexe Funktionen $f$ zu finden ist um ein vielfaches schwerer. Es gibt sog. *globale Optimierungsverfahren*, doch diese funktionieren nur für vergleichsweise kleine Probleme. In dieser Vorlesung behandeln wir sie nicht. In {ref}`sec:ml` werden wir sehen, dass der Verzicht auf globale Lösungen zumindest im Bereich maschinelles Lernen kein großes Problem ist.
````


## Allgemeines Framework
Der in {ref}`sec:gd-preview` vorgestellte Gradientenabstieg ist ein Vertreter einer ganzen Familie von Gradientenverfahren. Sie folgen alle einem bestimmten Aufbau, unterscheiden sich aber in der Ausgestaltung der einzelnen Schritte. Wie zuvor bezeichnen wir mit $k$ unseren Iterationszähler und wir schreiben $^{[k]}$ an jede Größe, die sich von Iteration zu Iteration ändern kann.

Bevor das allgemeine Verfahren aufschreiben, schauen wir uns zunächst noch einmal an, wie wir begründet haben, dass der Gradientenabstieg funktioniert. Wir haben das Taylor-Polynom erster Ordnung am Entwicklungspunkt $\v x^{[k]}$, der aktuellen Iterierten, aufgestellt (man sagt auch: die Funktion $f$ *linearisiert*) und damit den Funktionswert an der neuen Iterierten angenähert.

\ba  
f(\v x^{[k+1]})=f(\v x^{[k]}+\v d^{[k]})&\approx f(\v x^{[k]})+\nabla f(\v x^{[k]})\v d^{[k]}\\
&=f(\v x^{[k]})-\alpha^{[k]}\nabla f(\v x^{[k]})\nabla f(\v x^{[k]})^T\\
&=f(\v x^{[k]})-\underbrace{\alpha^{[k]}\norm{\nabla f(\v x^{[k]})}^2}_{>0}
\ea 
In Worten: Der Funktionswert am neuen Punkt $\v x^{[k+1]}$ ist kleiner als am aktuellen Punkt $\v x^{[k]}$, wenn als Schritt $\v d^{[k]}=-\alpha^{[k]}\nabla f(\v x^{[k]})$ gewählt wird (mit einer geeignete Schrittweite $\alpha^{[k]}>0$). Wenn man für $\v d^{[k]}$ den Gradienten wählt, kann auf jeden Fall ein Abstieg erzielt werden.

An der ersten Gleichung sieht man aber auch, dass eigentlich nur $\nabla f(\v x^{[k]})\v d^{[k]}<0$ gelten muss, um zu garantieren, dass sich der Funktionswert verringert (Voraussetzung nach wie vor: man bleibt nahe genug bei $\v x^{[k]}$, so dass die Linearisierung eine ausreichend gute Approximation ist). Interessant:  $\nabla f(\v x^{[k]})\v d^{[k]}$ ist die Richtungsableitung in Richtung $\v d^{[k]}$, siehe {ref}`sec:richtung`. Man nennt *jedes* $\v d^{[k]}$, für das gilt $\nabla f(\v x^{[k]})\v d^{[k]}<0$ eine *Abstiegsrichtung*. 

Wenn $\v d^{[k]}=\nabla f(\v x^{[k]})$ gewählt wird, so liefert dies zwar den kleinstmöglichen Wert $\nabla f(\v x^{[k]})\v d^{[k]}$, siehe {ref}`sec:interpretation`, aber die Linearisierung ist evtl. nur in einer sehr kleinen Umgebung von $\v x^{[k]}$ gültig. Oft ist es klüger, nicht den aktuell steilsten Abstieg zu wählen um längerfristig eine bessere Reduktion der Funktion zu finden.

Zur Notation : wir ziehen ab jetzt den skalaren Faktor $\alpha^{[k]}$ aus dem $\v d^{[k]}$ heraus, schreiben also $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$ statt $\v x^{[k+1]}=\v x^{[k]}+\v d^{[k]}$.

````{prf:algorithm} Allgemeines Framework Abstiegsverfahren
Gegeben: 
: Differenzierbare Funktion $f:\R^n\rightarrow\R$.

Gesucht: 
: Lokales Minimum von $f$.

**Algorithmus**:

Starte mit initialer Schätzung $\v x^{[0]}$, setze $k=0$.

Für $k=0,1,2,\dots$:
1. Überprüfe, ob $\v x^{[k]}$ die **Abbruchbedingung** erfüllt. 
    - Falls ja: Abbruch mit Lösung $\v x^{[k]}$
    - Falls nein: gehe zu Schritt 2.
2. Bestimme **Abstiegsrichtung** $\v d^{[k]}$ unter Verwendung lokaler Information (z.B. Gradient, Hessematrix)
3. Bestimme **Schrittweite** $\alpha^{[k]}$.
4. Berechne neue Iterierte $\v x^{[k+1]}=\v x^{[k]}+\alpha^{[k]}\v d^{[k]}$.
````
Es gibt viele Abstiegsverfahren, die sich darin unterscheiden, wie die Abstiegsrichtung $\v d$ und die Schrittweite $\alpha$ bestimmt werden. Außerdem gibt es unterschiedliche Abbruchbedingungen. Wir schauen uns diese Elemente in den folgenden Abschnitten an.
$\hyper{kkk}$

## Abbruchbedingungen

## Wahl der Schrittweite 
### Liniensuche
### Näherungsweise Liniensuche
### Dämpfung

## Probleme des Gradientenabstiegs

## Gradientenabstieg mit Momentum
### Nesterov Modifikation

