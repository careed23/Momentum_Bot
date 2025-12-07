#!/bin/bash

echo "🔄 Starting 90-second Loop for Momentum Bot..."

while true
do
    # 1. Run the bot wrapper we made earlier
    /home/creed/gemini-cli/run_bot.sh
    
    # 2. Print a timestamp so you know it ran
    echo "[$(date)] Bot run complete. Sleeping 90s..."
    
    # 3. Wait 30 seconds
    sleep 30
done
