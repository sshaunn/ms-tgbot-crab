#!/bin/bash
LOCK_FILE="/tmp/main_py_lock"

# Function to remove the lock file
cleanup() {
    rm -f "$LOCK_FILE"
}

# Set up trap to remove lock file on script exit
trap cleanup EXIT

# Check if the lock file exists
if [ -e "$LOCK_FILE" ]; then
    echo "Another instance of main.py is already running. Skipping main.py execution."
else
    # Create the lock file
    touch "$LOCK_FILE"

    # Run main.py once
    python main.py

    # Lock file will be automatically removed by the trap on exit
fi

# Add or update cron job (this will run every time start.sh is executed)
(crontab -l 2>/dev/null; echo "0 0 * * * $(pwd)/scheduler.sh") | crontab -

echo "Cron job for scheduler.sh has been added or updated."
