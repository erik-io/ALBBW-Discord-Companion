#!/bin/bash

sudo systemctl stop pythonDiscordBot.service

cd /home/ubuntu/pythonDiscordBot
git pull origin main

sudo systemctl start pythonDiscordBot.service