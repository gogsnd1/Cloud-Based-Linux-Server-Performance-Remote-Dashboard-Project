#!/bin/bash

SCRIPT_PATH="/home/gogsnd1/Cloud-Based-Linux-Server-Performance-Remote-Dashboard-Project/central-server/centralMonitor1.py"

PROCESS_NAME="centralMonitor1.py"

if ! pgrep -f "$PROCESS_NAME" > /dev/null
then
    echo "$(date): centralMonitor1.py is down. Restarting..." >> ~/centralMonitor.log
    nohup /usr/bin/python3 $SCRIPT_PATH > ~/centralMonitor_output.log 2>&1 &
else
    echo "$(date): centralMonitor1.py is running fine." >> ~/centralMonitor.log
fi
