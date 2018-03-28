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

/etc/init.d/$ADAPTERSERVICENAME stop
update-rc.d -f $ADAPTERSERVICENAME remove
#Clean up any old adapter stuff
echo "------Cleaning Up Old Adapter Configurations"
rm $INITDPATH/$ADAPTERSERVICENAME
#rm -rf $SCRIPTDIR

echo "------Removing System.d script"
#TODO

