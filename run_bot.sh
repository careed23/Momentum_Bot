#!/bin/bash

# 1. Load your API Keys
source /home/creed/env

# 2. Go to the folder
cd /home/creed/gemini-cli

# 3. Activate the Virtual Environment
source venv/bin/activate

# 4. Run the Bot and save logs to a file
python momentum_bot.py >> bot_activity.log 2>&1
