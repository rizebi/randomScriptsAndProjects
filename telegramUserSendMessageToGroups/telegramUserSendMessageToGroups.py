import os
import sys
import time # for sleep
import logging # for logging
import datetime # for logging
import traceback # for error handling
from telethon import TelegramClient, events, sync # for telegram use

## Author: Eusebiu Rizescu
## Email: rizescueusebiu@gmail.com

# pip3 install telethon

## Variables
api_id = "API_ID_TO_REPLACE"
api_hash = "API_KEY_TO_REPLACE"
messageFile = "message.txt" # Relative path to the message file that contains the text of the sending message
groupsFile = "groups.txt" # Relative path to the groups file. One groupName per line.
pictureFile = "picturePath.txt" # Relative path to the groups file. This file contians path to the image, or is empty
defaultSleepMinutesBetweenMessages = 3
sleepSecondsBetweenRuns = 30 # This should be lower that the smallest number of wait minutes for a group. 30 seconds is good.

## Needed variables
currentDir = os.getcwd()
lastUpdateEvent = 0

# Logging function
def getLogger():
  # Create logs folder if not exists
  if not os.path.isdir(os.path.join(currentDir, "logs")):
    try:
      os.mkdir(os.path.join(currentDir, "logs"))
    except OSError:
      print("Creation of the logs directory failed")
    else:
      print("Successfully created the logs directory")

  now = datetime.datetime.now()
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-telegramUserSendMessageToGroups.log"
  log_name = os.path.join(currentDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Function that sends a message to a groupName
def sendTelegramMessage(log, client, groupName):
  try:
    # Read message
    message = open(os.path.join(currentDir, messageFile), mode="r").read()
    picturePathToSend = open(os.path.join(currentDir, pictureFile), mode="r").read().replace(os.linesep, "").strip()
    if picturePathToSend == "":
      # Send only message
      client.send_message(groupName, message)
    else:
      # Send photo with caption
      client.send_file(groupName, picturePathToSend, caption=message)

    return True
  except Exception as e:
    log.info("Error when sending Telegram message: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    return False

# Function that read groups to send messages to from the file
# Groups file has the following format:
# my_special_group, 4    <- first is the groupName, then comma then the interval between messages
# or
# my_other_group       <- the groupName, and the default interval between messages will be used
def readGroups(log, oldDict):
  groups = open(os.path.join(currentDir, groupsFile), "r")
  groups = groups.read().split(os.linesep)

  groupsDict = {}
  # Get group name from
  for group in groups:
    group = group.strip()
    if group == "" or group == os.linesep:
      continue
    if "," in group:
      groupName = group.split(",")[0].strip()
      messageInterval = float(group.split(",")[1].strip())
    else:
      groupName = group
      messageInterval = defaultSleepMinutesBetweenMessages
    # Add the group to the dict
    if groupName in oldDict.keys():
      groupsDict[groupName] = {"messageInterval": messageInterval, "lastMessageTimestamp": oldDict[groupName]["lastMessageTimestamp"]}
    else:
      groupsDict[groupName] = {"messageInterval": messageInterval, "lastMessageTimestamp": 0}

  return groupsDict

# Main function
def mainFunction():
  log = getLogger()
  log.info("###################################################### New MAIN run")

  try:
    # Break if config files not found
    if os.path.isfile(os.path.join(currentDir, messageFile)) is False:
      log.info("Message file " + messageFile + " not found. Exiting.")
    if os.path.isfile(os.path.join(currentDir, groupsFile)) is False:
      log.info("Message file " + groupsFile + " not found. Exiting.")
    if os.path.isfile(os.path.join(currentDir, pictureFile)) is False:
      log.info("Message file " + pictureFile + " not found. Exiting.")

    # At the start we assume that we should send messages to all groups
    oldGroupsDict = {}

    # Instantiate Telegram client
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    # Main while
    while True:
      log.info("##################### New run")

      # Read the groups
      groups = readGroups(log, oldGroupsDict)

      log.info("Groups: " + str(groups))

      # Send the message
      for group in groups.keys():

        log.info("### Processing group: " + group)
        now = time.time()

        if now - groups[group]["lastMessageTimestamp"] < groups[group]["messageInterval"] * 60:
          log.info("Time interval not already passed. Wait " + str(groups[group]["messageInterval"] * 60 - (now - groups[group]["lastMessageTimestamp"])) + " seconds.")
        else:
          log.info("Time interval passed. Sending message")
          status = sendTelegramMessage(log, client, group)
          if status == True:
            log.info("Message successfully sent.")
            groups[group]["lastMessageTimestamp"] = now
          else:
            log.info("Error, message not sent.")

      oldGroupsDict = groups
      # Sleep between runs
      log.info("Sleeping " + str(sleepSecondsBetweenRuns) + " seconds.")
      time.sleep(sleepSecondsBetweenRuns)

  ##### END #####
  except KeyboardInterrupt:
    log.info("Quit")
    sys.exit(0)
  except Exception as e:
    log.info("Fatal Error: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    sys.exit(98)


##### BODY #####
if __name__ == "__main__":

  if len(sys.argv) != 1:
    log.info("Wrong number of parameters. Use: python telegramUserSendMessageToGroups.py")
    sys.exit(99)
  else:
    mainFunction()
