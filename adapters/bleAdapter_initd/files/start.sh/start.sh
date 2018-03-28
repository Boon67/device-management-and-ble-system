#!/bin/bash
if [ "$EUID" -ne 0 ]
  then 
  	echo "---------Permissions Error---------"
  	echo "STOPPING: Please run as root or sudo"
  	echo "-----------------------------------"
  exit
fi
#Bring BLE Adapter Up
hciconfig hci0 up

SCRIPTDIR="${0%/*}"
CONFIGFILENAME="adapterconfig.txt"
source "$SCRIPTDIR/$CONFIGFILENAME"

/etc/init.d/$ADAPTERSERVICENAME start
