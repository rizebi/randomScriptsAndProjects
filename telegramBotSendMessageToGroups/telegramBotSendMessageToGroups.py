import os
import sys
import time # for sleep
import logging # for logging
import datetime # for logging
import requests # for Telegram API manipulation
import traceback # for error handling

# pip3 install requests

# Todo for windows

## Variables
currentDir = os.getcwd()
groupsFile = "groups.txt" # Relative path to the groups file. One group per line. to set a different sleep time between messages, other than the default one, add at the end of group name TODO ", X", and replace X with the number of minutes
messageFile = "message.txt" # Relative path to the message file that contains the text of the sending message
picture = "" # Path to picture. Leave "" if no picture attached
groupsMappingFile = "mapping.txt"
defaultSleepMinutesBetweenMessages = 0.05 #TODO replace with 3
sleepSecondsBetweenRuns = 5 #TODO # This should be lower that the smallest number of wait minutes for a group. 30 seconds is good.
botToken = "REPLACE_BOT_NAME"

# https://api.telegram.org/bot1648992630:AAE4-4yvsvBilhCqMB8d_w1MHU0Fxr9wmX0/getUpdates

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
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Read the group mapping files to get the already known chat ids
# A line in group mapping file is:
# Name: <<<My_Group_X>>>, ChatId: <<<1938451051>>>
def readGroupsMapping(log):
  groupsMappings = open(os.path.join(currentDir, groupsMappingFile), "r")
  groupsMappings = groupsMappings.read().split("\n")
  alreadyKnownGroups = []
  # Get group name from
  for groupMapping in groupsMappings:
    groupMapping = groupMapping.strip()
    if groupMapping == "" or groupMapping == "\n":
      continue
    try:
      groupName = groupMapping.split("<<<")[1].split(">>>")[0]
      alreadyKnownGroups.append(groupName)
    except Exception as e:
      log.info("ERROR when reading from group mapping, when processing: " + groupMapping)
      tracebackError = traceback.format_exc()
      log.info(tracebackError)

  return alreadyKnownGroups

# For each run, get the updates of the bot and update the group mapping file with the new
# chat_ids. When a bot is added to a group, an update is accessible, and we parse that, and
# add the chat id to the group mapping file
def updateGroupsMapping(log):

  try:
    alreadyKnownGroups = readGroupsMapping(log)
    response = requests.get("https://api.telegram.org/bot" + botToken + "/getUpdates")
    response = response.json()
    # For each update, try to get if the bot was added in a group
    for update in response["result"]:
      if "my_chat_member" not in update:
        continue
      # Get the groupName and chatId
      groupName = update["my_chat_member"]["chat"]["title"]
      chatId = str(update["my_chat_member"]["chat"]["id"])
      log.info("Bot was added to group: " + groupName + " with chat id: " + chatId)
      if groupName in alreadyKnownGroups:
        log.info("We already have this group in mapping groups file")
      else:
        log.info("This is a new group, add it to the group mapping file")
        with open(os.path.join(currentDir, groupsMappingFile), 'a') as file:
          file.write("Name: <<<" + groupName + ">>>, ChatId: <<<" + chatId + ">>>\n")

  except Exception as e:
    log.info("Error when getting Updates for bot: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)

# Function that read domains from the file
def readGroups(log):
  domainsList = open(os.path.join(currentDir, domainsFile), "r") # Read data
  domainsList = domainsList.read().split("\n")
  log.info(domainsList)
  # Remove spaces and cast to lowercase
  i = 0
  while i < len(domainsList):
    domainsList[i] = domainsList[i].strip().lower()
    domainsList[i] = domainsList[i].replace("https://", "")
    domainsList[i] = domainsList[i].replace("/", "")
    i += 1
  # Remove "\n" from list
  while "\n" in domainsList:
    domainsList.remove("\n")
  # Remove "" from list
  while "" in domainsList:
    domainsList.remove("")
  log.info(domainsList)
  return domainsList


# Main function
def mainFunction():
  log = getLogger()
  log.info("###################################################### New MAIN run")

  try:
    # Main while
    while True:
      log.info("##################### New run")
      # Read the groups
      # groups = readGroups(log)

      # Get bot updates in order to see if the bot was added to a new group.
      updateGroupsMapping(log)

      # Sleep between runs
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
    log.info("Wrong number of parameters. Use: python telegramBotSendMessageToGroups.py.py")
    sys.exit(99)
  else:
    mainFunction()
