#!/bin/bash

PIPE="/tmp/stats_pipe"

# Create the named pipe if it doesn't exist
if [ ! -p "$PIPE" ]; then
  mkfifo "$PIPE"
  echo "Named pipe created at $PIPE"
fi

# Continuously write simulated metrics to the pipe
while true; do
  TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
  # Simulate CPU load: grab the 1-minute load average from /proc/loadavg
  CPU_LOAD=$(awk '{print $1}' /proc/loadavg)
  # Simulate Memory usage: calculate percentage from free memory (for example purposes)
  MEM_USAGE=$(free | awk '/Mem/ {printf "%.2f", $3/$2*100}')
  
  METRIC="$TIMESTAMP - CPU Load: $CPU_LOAD, Memory Usage: $MEM_USAGE%"
  echo "$METRIC" > "$PIPE"
  
  sleep 2
done
