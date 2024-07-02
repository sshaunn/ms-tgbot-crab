#!/bin/bash
# Find the PID of the Python process running main.py
crontab -l | grep -v "$CRON_JOB" | crontab -
echo "Cron job removed."
pid=$(pgrep -f "python main.py")

if [ -n "$pid" ]; then
    echo "Stopping Python process (PID: $pid)"
    kill $pid

    # Wait for a moment and check if the process has stopped
    sleep 2
    if ps -p $pid > /dev/null; then
        echo "Process did not stop gracefully. Forcing stop."
        kill -9 $pid
    else
        echo "Process stopped successfully."
    fi
else
    echo "No Python process running main.py found."
fi

python main.py
(crontab -l 2>/dev/null; echo "0 0 * * * $(pwd)/project/src/scheduler.sh") | crontab -
echo "Cron job for scheduler.sh has been added or updated."

#LOCK_FILE="/tmp/main_py_lock"
#
## Function to remove the lock file
#cleanup() {
#    rm -f "$LOCK_FILE"
#}
#
## Set up trap to remove lock file on script exit
#trap cleanup EXIT
#
## Check if the lock file exists
#if [ -e "$LOCK_FILE" ]; then
#    echo "Another instance of main.py is already running. Skipping main.py execution."
#else
#    # Create the lock file
#    touch "$LOCK_FILE"
#
#    # Run main.py once
#    python main.py
#    (crontab -l 2>/dev/null; echo "0 0 * * * $(pwd)/project/src/scheduler.sh") | crontab -
#    echo "Cron job for scheduler.sh has been added or updated."
#    # Lock file will be automatically removed by the trap on exit
#fi
