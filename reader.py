#!/usr/bin/env python3
import os

pipe_path = "/tmp/stats_pipe"

# Check if the named pipe exists
if not os.path.exists(pipe_path):
    print(f"Named pipe {pipe_path} does not exist. Please run the writer script first.")
    exit(1)

print(f"Listening for data on {pipe_path}...")

with open(pipe_path, "r") as pipe:
    while True:
        line = pipe.readline()
        if line:
            print("Received:", line.strip())
