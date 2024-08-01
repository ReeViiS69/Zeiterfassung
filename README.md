Consolen-Python "Programm"(script)

Ursprünglich habe ich es in einfachster Form mit Start- und Endzeiten verwendet, um fehlerhafte Korrekturen in der Firmenlösung nachzuhalten. 
Nachdem ich aber wieder Spaß daran gefunden hatte, kamen mir Ideen, wie ich das Ganze noch optimieren konnte. Zuerst kamen die Pausen hinzu,
dann der Code zum Erkennen, ob jetzt Pause oder Zeit gesetzt werden sollte, und zuletzt eine Möglichkeit, um den heutigen abgeschlossenen Tag auch wieder zu eröffnen.

Aktuell sind mir keine Bugs bekannt, aber das heißt nur, dass ich nicht alles weiß und kann. Ich habe versucht, möglichst wenige Importe von Helfern zu nutzen.
Ein Script zur Auswertung folgt; aktuell ist es nicht für die Version 1.0 angepasst.
Eine Version mit Datenbank ist nicht geplant.

todo: zweite version oder config möglichkeit hinzufügen um eine version zuerstellen die mit der deutschen datumsformatierung dd.mm.yyyy hh:mm:ss kompatibel ist. aktuell yyyy-mm-dd hh:mm:ss
daher aktuell nur editierbar in editor oder notepad, newline ist nicht schuld, da script richtigerweise dd.mm.yyyy != yyyy.mm.dd erkennt
eventuell reicht datetime strp und strf befehle anpassen
