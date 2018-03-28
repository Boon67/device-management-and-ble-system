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

systemctl stop $ADAPTERSERVICENAME