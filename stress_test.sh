#!/bin/bash

CPU_LOAD_TIME=30
MEM_LOAD_TIME=30
IO_LOAD_TIME=30
FS_LOAD_TIME=30
VM_LOAD_TIME=30

echo "Starting system stress test..."
#stress cpu with 4 workers for 30 secs
stress-ng --cpu 4 --timeout ${CPU_LOAD_TIME}s &
sleep 5
#stress memory with 2GB allocated for 30 secs
stress-ng --vm 2 --vm-bytes 2G --timeout ${MEM_LOAD_TIME}s &
sleep 5

#stress I/O operations
stress-ng --io 4 --timeout ${IO_LOAD_TIME}s &
sleep 5

#stress File System
stress-ng --hdd 2 --timeout ${FS_LOAD_TIME}s &
sleep 5

#Stress virtual memory
stress-ng --vm 1 --vm-bytes 1G --timeout ${VM_LOAD_TIME}s &

echo "System stress test complete."
 

