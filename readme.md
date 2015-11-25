# Braubar

Hey there, this is Braubar!


## Deployment

Aktuell läuft das Deployment über einen git post-receive hook. 
                                                                                               
 #!/bin/sh 
 
 DEPLOYDIR=~/apps/braubar
 GIT_WORK_TREE="$DEPLOYDIR" git checkout -f
 cd "$DEPLOYDIR" 
 
 # Do some python magic!
 
 source $DEPLOYDIR/deployment/deplo.sh
 echo "Alimost everything done, except installing python for the hook! ;)"
 
Der wiederum ein Skript (deploy.sh) aus dem deployment Verzeichnis aufruft.
