import os
import sys
import time # for sleep
import json # for json manipulation
import random # for creation of the message
import asyncio # for async
import logging # for logging
import datetime # for logging
import traceback # for error handling
from telethon import TelegramClient # for telegram use

from telethon.errors.rpcerrorlist import ChatWriteForbiddenError, SlowModeWaitError, UserBannedInChannelError, ChannelPrivateError, FloodWaitError, ChatRestrictedError # telegram errors

## Author: Eusebiu Rizescu
## Email: rizescueusebiu@gmail.com

# pip3 install telethon

## Variables
api_id = "---"
api_hash = "---"

messageFile = "message.txt" # Relative path to the message file that contains the text of the sending message
groupsFile = "groups.txt" # Relative path to the groups file. One chat id per line.
sleepMinutesBetweenMessagesInAGroup = 1440 # One message per day (1440 = 24 hours)
sleepMinutesBetweenEachMessageSent = 20

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
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-telegramBotSendMessageToGroups.py.log"
  log_name = os.path.join(currentDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.INFO,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Function that will compose a message based on the JSON
def composeMessage(log, coinName):
  messageObj = json.load(open(os.path.join(currentDir, messageFile), mode="r"))
  message = ""
  for chunk in messageObj["chunks"]:
    message += random.choice(chunk) + " "

  message = message.replace("<<coin>>", coinName)

  return message

# Function that sends a message to a chatId
async def sendTelegramMessage(log, chatId, coinName):
  global lastMessageStatus

  try:
    # Compose message
    message = composeMessage(log, coinName)
    # Send message
    await telegramClient.send_message(int(chatId), message)

    lastMessageStatus = True

  except ChatWriteForbiddenError:
    log.info("Error <ChatWriteForbiddenError> when trying to send message to: " + chatId)
    time.sleep(15)
    lastMessageStatus = False

  except SlowModeWaitError:
    log.info("Error <SlowModeWaitError> when trying to send message to: " + chatId)
    time.sleep(30)
    lastMessageStatus = False

  except ChatRestrictedError:
    log.info("Error <ChatRestrictedError> when trying to send message to: " + chatId)
    time.sleep(30)
    lastMessageStatus = False

  except ChannelPrivateError:
    log.info("Error <ChannelPrivateError> when trying to send message to: " + chatId)
    time.sleep(90)
    lastMessageStatus = False

  except UserBannedInChannelError:
    log.info("Error <UserBannedInChannelError> when trying to send message to: " + chatId)
    time.sleep(7200)
    lastMessageStatus = False

  except FloodWaitError:
    log.info("Error <FloodWaitError> when trying to send message to: " + chatId)
    time.sleep(450)
    lastMessageStatus = False

  except Exception as e:
    log.info("Error when sending Telegram message: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    lastMessageStatus = False

# Function that read groups to send messages to from the file
# Groups file has the following format:
# 23235324, 4    <- first is the chat id, then comma then the interval between messages
# or
# 34534534       <- the chat id, and the default interval between messages will be used
def readGroups(log, oldDict):
  log.info("##### Run readGroups")
  groups = open(os.path.join(currentDir, groupsFile), "r")
  groups = groups.read().split(os.linesep)

  groupsDict = {}
  # Get group name from
  for group in groups:
    group = group.strip()
    if group == "" or group == os.linesep:
      continue
    if len(group.split(",")) != 2:
      log.info("Skipping group: " + group + " because is not well formatted")
      continue

    chatId = group.split(",")[0].replace(" ", "")
    coinName = group.split(",")[1].replace(" ", "")
    messageInterval = sleepMinutesBetweenMessagesInAGroup
    # Add the group to the dict
    if chatId in oldDict.keys():
      groupsDict[chatId] = {"messageInterval": messageInterval, "coinName": coinName, "lastMessageTimestamp": oldDict[chatId]["lastMessageTimestamp"]}
    else:
      groupsDict[chatId] = {"messageInterval": messageInterval, "coinName": coinName, "lastMessageTimestamp": 0}

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
      log.info("Groups file " + groupsFile + " not found. Exiting.")

    # Start the Telegram client
    log.info("Start client")
    global telegramClient
    telegramClient = TelegramClient("bot", api_id, api_hash)
    telegramClient.start()


    # At the start we assume that we should send messages to all groups
    oldGroupsDict = {}

    # Main while
    while True:
      log.info("##################### New run")

      # Read the groups
      groups = readGroups(log, oldGroupsDict)

      log.info("Groups: " + str(groups))

      # Get the group with the oldest message sent
      oldestGroup = ""
      minimumTimestamp = time.time()
      for group in groups.keys():
        if groups[group]["lastMessageTimestamp"] < minimumTimestamp:
          oldestGroup = group
          minimumTimestamp = groups[group]["lastMessageTimestamp"]
      group = oldestGroup

      if group != "":
        log.info("### Processing group: " + group)

        now = time.time()
        if now - groups[group]["lastMessageTimestamp"] < groups[group]["messageInterval"] * 60:
          log.info("Time interval not already passed. Wait " + str(groups[group]["messageInterval"] * 60 - (now - groups[group]["lastMessageTimestamp"])) + " seconds.")
        else:
          log.info("Time interval passed. Sending message")
          loop = asyncio.get_event_loop()
          coroutine = sendTelegramMessage(log, group, groups[group]["coinName"])
          loop.run_until_complete(coroutine)

          if lastMessageStatus == True:
            log.info("Message successfully sent.")
          else:
            log.info("Error, message not sent.")

          # Update timestamp regardless of the status in order to not stuck on a grup
          groups[group]["lastMessageTimestamp"] = now

      oldGroupsDict = groups
      # Now, we need to sleep in order to not send messages in all the groups from config at once.
      log.info("Sleeping " + str(sleepMinutesBetweenEachMessageSent * 60) + " seconds because we have finished a complete cycle between groups / send a message.")
      time.sleep(sleepMinutesBetweenEachMessageSent * 60)

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
    log.info("Wrong number of parameters. Use: python telegramBotSendMessageToGroups.py")
    sys.exit(99)
  else:
    mainFunction()
