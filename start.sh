#!/bin/bash
# Find the PID of the Python process running main.py
#crontab -l | grep -v "$CRON_JOB" | crontab -
#echo "Cron job removed."
#pid=$(pgrep -f "python main.py")
#
#if [ -n "$pid" ]; then
#    echo "Stopping Python process (PID: $pid)"
#    kill $pid
#
#    # Wait for a moment and check if the process has stopped
#    sleep 2
#    if ps -p $pid > /dev/null; then
#        echo "Process did not stop gracefully. Forcing stop."
#        kill -9 $pid
#    else
#        echo "Process stopped successfully."
#    fi
#else
#    echo "No Python process running main.py found."
#fi

python main.py
#(crontab -l 2>/dev/null; echo "0 0 1,* * * $(pwd)/project/src/scheduler.sh") | crontab -
#echo "Cron job for scheduler.sh has been added or updated."
