#! /bin/bash

echo "Start bot"
nohup python3 -u telegramBot.py > telegramBot.py.log 2>&1 &
echo "Bot started"
