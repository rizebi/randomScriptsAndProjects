#! /bin/bash

echo "Start bot"
nohup python3 -u telegramBotSendMessageToGroups.py > telegramBotSendMessageToGroups.py.log 2>&1 &
echo "Bot started"
