#!/bin/bash
# This script is used to update the bot from the main branch

# Stop the bot
cd /home/ubuntu/pythonDiscordBot || exit
pm2 stop pythonDiscordBot

# Pull the latest changes
git reset --hard
git pull origin main

# Activate the virtual environment
source venv/bin/activate

# Install the latest dependencies
pip install -r requirements.txt

# Restart the bot
pm2 stahonDiscordBot --interpreter=python3