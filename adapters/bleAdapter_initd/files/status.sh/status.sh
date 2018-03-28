#!/bin/bash
if [ "$EUID" -ne 0 ]
  then 
  	echo "---------Permissions Error---------"
  	echo "STOPPING: Please run as root or sudo"
  	echo "-----------------------------------"
  exit
fi

SCRIPTDIR="${0%/*}"
CONFIGFILENAME="adapterconfig.txt"
source "$SCRIPTDIR/$CONFIGFILENAME"
# If this script is executed, we know the adapter has been deployed. No need to test for that.
STATUS="Deployed"

PID=$(pgrep $ADAPTERSERVICENAME)
#echo $PID
if [[ $PID ]]; then
	STATUS="Running $PID"
else
	STATUS="Stopped"
fi

echo $STATUS
