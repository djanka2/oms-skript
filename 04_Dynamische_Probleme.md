(sec:zeitdiskret)=
# Zeitdiskrete Modelle

Wir betrachten in diesem Kapitel Probleme, bei denen sich die Entscheidungsmöglichkeiten über einen gewissen Zeithorizont erstrecken. Wir betrachten folgendes Beispiel:


## Energiespeicher
````{prf:example}
Ein Unternehmen kann gut vorhersagen, wann es wieviel Strom benötigt. Das Unternehmen bezieht den Strom durch einen Versorger. Der Strompreis wechselt über die Zeit, ist vorher aber bekannt. Zusätzlich hat das Unternehmen einen Batteriespeicher installiert. So kann das Unternehmen Strom in die Batterie einspeichern, wenn der Strompreis niedrig ist und den Strom wieder ausspeichern und selbst verbrauchen, wenn der Strom teuer ist. Das Unternehmen möchte den Batteriespeicher optimal nutzen.

\Karos{33}{28}
````

Ein gängiges Vorgehen bei dieser Problemklasse ist die *Zeitdiskretisierung*: Die Zeit wird in gleichlange Zeitscheiben eingeteilt. Innerhalb einer Zeitscheibe werden alle Werte als konstant angenommen. Je kürzer die Zeitscheiben sind, desto genauer wird das Problem modelliert. Mit höherer Detailtreue steigt aber auch der Rechenaufwand um das Modell zu lösen.

Für die Modellierung wählen wir Zeitscheiben von einer Stunde Länge. Die Modellierungsgenauigkeit orientiert sich in diesem Fall am Strompreis. Dieser ändert sich jede Stunde und die zeitabhängige Abrechnung erfolgt in dieser Auflösung.

Es sind folgende Daten gegeben:
- Ein betrachteter Zeithorizont $\{1,2, \ldots, 24\}$ von einem Tag.
- Der Verbrauch $d_t$ zum Zeitpunkt $t$. 
- Der Strompreis $p_t$ zum Zeitpunkt $t$.
- Die Kapazität $s_{max}$ des installierten Batteriespeichers.  
- Der initiale Füllstand $s_0$ des installierten Batteriespeichers.
Wir nutzen folgende Entscheidungsvariablen
- Den Strombezug $k_t$ vom Netzbetreiber zum Zeitpunkt $t$.
- Die Einspeicherung $s^+_t$ in den Batteriespeicher zum Zeitpunkt $t$.
- Die Ausspeicherung $s^-_t$ aus dem Batteriespeicher zum Zeitpunkt $t$.
- Den Speicherstand $s_t$ zum Zeitpunkt $t$.
Dies führt zu folgender Modellierung:

````{prf:example}
TO DO
````

In kurzer Schreibweise ergibt sich
\begin{alignat*}{5}
\min & \quad  &   \sum_{t=1}^{24}p_tk_t &          & & \\[4mm]
\text{s.t. } & & k_t + s^- - s^+  & =  & \quad d_t & \quad\quad & & \forall t= 1, \ldots, 24 \\[2mm]
& & s_{t-1} - s^- + s^+  & = & s_t & & & \forall t= 1, \ldots, 24 \\[3mm]
& & s_t & \leq & \quad s_{max} & && \forall t= 1, \ldots, 24. \\
& & s_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24. \\
& & k_t & \geq & \quad 0 & && \forall t= 1, \ldots, 24.
\end{alignat*}
Das Ergebnis einer Beispielrechnung ist

```{figure} ./bilder/BeispielBatterie.png
:name: NichtlineareFunktionFuerApproximation
:height: 300px

Ergebnis zeitabhängiges lineare Optimierungsproblem.
```

## Produktionsplanungsproblem

## Kraftwerkeinsatzplanung

## MILP als Policy für ein dynamisches Problem
### Rollierendes Fenster Ansatz
### Evaluierung der Zielfunktion
### Umgang mit Unsicherheiten 


