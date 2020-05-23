#!/usr/bin/python3

import sys
import subprocess  # For executing a shell command
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setwarnings(False)
GPIO.output(23, False)

def ping(host):
  command = ['ping', "-W", "5", "-c", "1", host]
  return subprocess.call(command) == 0


def set_relay_state(relay1):
 if relay1 == "1":
   GPIO.output(23, True)
 else:
   GPIO.output(23, False)

if __name__ == "__main__":
  if ping("192.168.100.150") == False:
    set_relay_state("1")
    sleep(1)
    set_relay_state("0")
    sleep(1)
    sys.exit(0)
  else:
    sys.exit(99)
