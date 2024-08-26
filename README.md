Big Thanks to the Team behind Pyinstaller, im new to this and really didnt found the right way to give credit, so please inform me on nessesary changes!

Visit:
https://github.com/pyinstaller/pyinstaller/
https://pyinstaller.org
, to learn more about them to compile python to windows executable

HOW TO USE:
2 Modes: 
1.Custom filename ( was planned to only use for single tasks)
enter name-> currenttime gets saved, rerun script to enter endtime.(legacy (enter p) to pause cant work because limited user inputs possible, i guess the new reopen today function could work, but didnt tested it)

2.Main Mode: Filename is automaticly created by year-month_loggedinuser_time_log.csv
it should be kinda smart, you can enter p for pause or nothing for timestamp
you could enter what ever, because pause or time will always chosen right
in release1.1 it also checks if you forgot to end the last day, so you can enter a custom time, before opening another day thru rerunning the program

default is always to press enter!


BACKSTORY:
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


