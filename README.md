Consolen-Python "Programm"(script)

Ursprünglich habe ich es in einfachster Form mit Start- und Endzeiten verwendet, um fehlerhafte Korrekturen in der Firmenlösung nachzuhalten. 
Nachdem ich aber wieder Spaß daran gefunden hatte, kamen mir Ideen, wie ich das Ganze noch optimieren konnte. Zuerst kamen die Pausen hinzu,
dann der Code zum Erkennen, ob jetzt Pause oder Zeit gesetzt werden sollte, und zuletzt eine Möglichkeit, um den heutigen abgeschlossenen Tag auch wieder zu eröffnen.

Aktuell sind mir keine Bugs bekannt, aber das heißt nur, dass ich nicht alles weiß und kann. Ich habe versucht, möglichst wenige Importe von Helfern zu nutzen.
Ein Script zur Auswertung folgt; aktuell ist es nicht für die Version 1.0 angepasst.
Eine Version mit Datenbank ist nicht geplant.
Eine Excel(de-de) kompatible Version war geplant, aber dadurch wird ein großteil der Logik des Scripts unwirksam, weil alle Zeilen soviele Spalten bekommen wie die längste zeile.->View only!

Stundenrechner ist aktuell für 6Stunden eingestellt und wertet wochendtage nicht in die gearbeiteten tage-> nur überstunden am wochenende möglich

todo: Auswertung von Stundenrechner in .csv schreiben
late todo: configfile für time_log_monthly und stundenrechner implementieren, einstellungen sind aktuell im quelltext hardcoded und nicht als constanten angelegt
