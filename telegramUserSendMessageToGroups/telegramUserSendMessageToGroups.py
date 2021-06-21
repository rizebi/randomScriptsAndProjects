import os
import sys
import time # for sleep
import codecs # for emoji support
import logging # for logging
import datetime # for logging
import traceback # for error handling
from telethon import TelegramClient, events, sync # for telegram use

## Author: Eusebiu Rizescu
## Email: rizescueusebiu@gmail.com

# pip3 install telethon

## Variables
api_id = "6019497"
api_hash = "d20d859a1504390e1e3a2b5b2210c2aa"
groupsFile = "groups.txt" # Relative path to the groups file. One groupName per line.
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
def sendTelegramMessage(log, client, groupName, messageFile, imageFile):
  try:
    # Read message
    message = codecs.open(os.path.join(currentDir, messageFile), mode="r", encoding='utf-8').read()

    if imageFile == "":
      # Send only message
      client.send_message(groupName, message)
    else:
      # Send photo with caption
      client.send_file(groupName, imageFile, caption=message)

    return True
  except Exception as e:
    log.info("Error when sending Telegram message: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    return False

# Function that read groups to send messages to from the file
# Groups file has the following format:
# my_special_group, 4, path_to_message, optional_path_to_image    <- first is the groupName, interval, path to message, path to image
def readGroups(log, oldDict):
  groups = open(os.path.join(currentDir, groupsFile), "r")
  groups = groups.read().replace("\r\n", os.linesep).replace("\n", os.linesep).split(os.linesep)

  groupsDict = {}
  # Get group name from
  for group in groups:
    group = group.strip()
    if group == "" or group == os.linesep:
      continue
    groupName = group.split(",")[0].strip()
    messageInterval = float(group.split(",")[1].strip())
    messageFile = group.split(",")[2].strip()
    if len(group.split(",")) == 4:
      imageFile = group.split(",")[3].strip()
    else:
      imageFile = ""


    # Add the group to the dict
    groupsDict[groupName] = {"messageInterval": messageInterval, "messageFile": messageFile, "imageFile": imageFile}
    if groupName in oldDict.keys():
      groupsDict[groupName]["lastMessageTimestamp"] = oldDict[groupName]["lastMessageTimestamp"]
    else:
      groupsDict[groupName]["lastMessageTimestamp"] = 0

  return groupsDict

# Main function
def mainFunction():
  log = getLogger()
  log.info("###################################################### New MAIN run")

  try:
    # Break if config files not found
    if os.path.isfile(os.path.join(currentDir, groupsFile)) is False:
      log.info("Groups file " + groupsFile + " not found. Exiting.")

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
          status = sendTelegramMessage(log, client, group, groups[group]["messageFile"], groups[group]["imageFile"])
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
