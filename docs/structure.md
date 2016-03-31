# Structure

Generally braubar is divided into three parts: 

- Brewdaemon
- Socketserver
- Webserver

## Brewdaemon

The Brewdaemon manages the whole application and starts the Socketserver
and the Webserver as subprocesses. 
It keeps track of the current state. 


- entscheidet über heizen
- liest temp werte aus datei aus


### State 

- Verschiedene Phasen beim kochen. 
- infos für states aus der config


## Socketserver

- empfängt temperaturdaten vom arduino
- schreibt daten in eine datei
 
