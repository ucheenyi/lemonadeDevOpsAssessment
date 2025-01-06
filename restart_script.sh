#!/bin/bash

# Threshold CPU usage (in percentage) for restarting the service
CPU_THRESHOLD=80

# Service name for the Laravel backend (adjust to your actual service name)
LARAVEL_SERVICE="your-laravel-backend-service"

# Get the current CPU usage as a percentage (top command, skipping the first row)
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

echo "Current CPU usage: $CPU_USAGE%"

# Check if the CPU usage exceeds the threshold
if (( $(echo "$CPU_USAGE > $CPU_THRESHOLD" | bc -l) )); then
    echo "CPU usage exceeds $CPU_THRESHOLD%. Restarting the Laravel backend service..."
    
    # Restart the Laravel service (modify as needed for your system)
    systemctl restart $LARAVEL_SERVICE
    
    if [ $? -eq 0 ]; then
        echo "Laravel service restarted successfully."
    else
        echo "Failed to restart the Laravel service."
    fi
else
    echo "CPU usage is below $CPU_THRESHOLD%. No action required."
fi
