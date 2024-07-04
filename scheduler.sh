#!/bin/bash
curl -X GET http://0.0.0.0:5000/api/admin/scheduler
echo "scheduler triggered, sending "
#crontab -e