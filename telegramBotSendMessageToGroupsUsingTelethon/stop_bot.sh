#! /bin/bash

echo "Stop telegramBotSendMessageToGroups.py"
kill -kill $(ps -eaf | grep "python3 -u telegramBotSendMessageToGroups.py" | grep -v grep | tr -s " " | cut -d " " -f 2)
echo "Bot stopped"
