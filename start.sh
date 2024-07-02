#!/bin/bash
python main.py
(crontab -l 2>/dev/null; echo "0 0 * * * ./scheduler.sh") | crontab -
