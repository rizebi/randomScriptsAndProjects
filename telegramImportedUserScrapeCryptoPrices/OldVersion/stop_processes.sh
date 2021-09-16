#! /bin/bash
echo "Stop updateData.py"
kill -kill $(ps -eaf | grep "python3 -u updateData.py" | grep -v grep | tr -s " " | cut -d " " -f 2)
echo "Stop tg.py"
kill -kill $(ps -eaf | grep "python3 -u tg.py" | grep -v grep | tr -s " " | cut -d " " -f 2)
echo "Processes stopped"
