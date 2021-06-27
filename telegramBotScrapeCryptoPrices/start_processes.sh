#! /bin/bash
nohup python3 -u updateData.py > updateData.py.log 2>&1 &
nohup python3 -u tg.py > tg.py.log 2>&1 &
echo "Processes started"
