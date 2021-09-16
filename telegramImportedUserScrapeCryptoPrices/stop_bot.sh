#! /bin/bash

echo "Stop telegramBot.py"
kill -kill $(ps -eaf | grep "python3 -u telegramBot.py" | grep -v grep | tr -s " " | cut -d " " -f 2)
echo "Bot stopped"
