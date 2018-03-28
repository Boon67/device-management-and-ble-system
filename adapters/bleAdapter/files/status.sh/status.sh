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

TARGETS=("$ADAPTERFULLPATH/$PYTHONFILE")
for target in "${TARGETS[@]}"
do
      PID=$(ps aux | grep -v grep | grep $target | awk '{print $2}')
      #echo $PID
		if [[ $PID ]]; then
		    STATUS="Running $PID"
		else
		    STATUS="Stopped"
		fi

echo $STATUS
done