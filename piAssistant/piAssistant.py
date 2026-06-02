import os
import json
import time
import logging # for logging
import datetime # for logging
import subprocess # for executing commands
from pathlib import Path # to read the password file
import urllib.request as request # to send messages
logging.getLogger('telethon').setLevel(logging.ERROR) # to avoid telethon log spam
from telethon import TelegramClient, events # to receive messages

currentDir = os.getcwd()
configFile = open("config.json")
config = json.load(configFile)

botToken = os.getenv(config["secretsEnv"]["botToken"])
apiId = os.getenv(config["secretsEnv"]["apiId"])
apiHash = os.getenv(config["secretsEnv"]["apiHash"])
channelIdList = [int(os.getenv(config["secretsEnv"]["channelId"]))]
client = TelegramClient('bot', apiId, apiHash)

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
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-piAssistant.log"
  log_name = os.path.join(currentDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

def executeCommand(log, command):
  error = ""
  output = ""
  log.info("Executing: " + command)
  try:
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
  except Exception as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e)  # to get the output even when error
  try:
    output = output.decode('utf-8')
  except:
    pass

  return output, error

def sendMessage(log, message):
  log.info("Sending message: " + message)
  # Create the payload
  payload = {"chat_id": channelIdList[0], "text": message }
  # Create the request
  requestObj = request.Request( "https://api.telegram.org/bot" + botToken + "/sendMessage",
    data=json.dumps(payload).encode('utf8'),
    headers={"Content-Type": "application/json"})
  # Send the message
  sendMessage = request.urlopen(requestObj)
  result = json.loads(sendMessage.read().decode())["result"]
  log.info(result)

def runRemote(log, instructions, host, messageList):
  # Get password
  sshPasswordText = os.getenv(host["pass"])
  # Remove backslashes (this is in order to work on both local laptop and server)
  sshPasswordText = sshPasswordText.replace("\\", "")

  # Replace arguments in instructions command
  instructionsCommand = instructions["command"]
  commandParametersCount = 0
  for i in range(1, 10):
    try:
      if "$" + str(i) in instructionsCommand:
        commandParametersCount += 1
      instructionsCommand = instructionsCommand.replace("$" + str(i), "\"" + messageList[i] + "\"")
    except:
      pass
  if commandParametersCount != len(messageList) - 1:
    return "", "Wrong number of parameters received."

  # Execute the command
  command = "sshpass -p '" + sshPasswordText + "' ssh -o StrictHostKeyChecking=no -p " + host["port"] + " "+ host["user"] + "@" + host["ip"] + " " + instructionsCommand
  output, error = executeCommand(log, command)
  log.info("Output = " + str(output))
  log.info("Error = " + str(error))

  return str(output).replace(sshPasswordText, "SECRET"), str(error).replace(sshPasswordText, "SECRET")

def getKnownCommands(log):
  knownCommands = "Rarely used commands:\n"
  for command in config["commands"].keys():
    if config["commands"][command]["hidden"] == "true":
      knownCommands += command + " " + config["commands"][command]["parameters"] + "\n"

  knownCommands += "\nUsual commands:\n"
  for command in config["commands"].keys():
    if config["commands"][command]["hidden"] == "false":
      knownCommands += command + " " + config["commands"][command]["parameters"] + "\n\n"

  return knownCommands

def sendKnownCommands(log):
  knownCommands = getKnownCommands(log)
  sendMessage(log, knownCommands)

def processMessage(log, receivedMessage):
  messageList = receivedMessage.split(" ")
  if messageList[0] in config["commands"].keys():
    instructions = config["commands"][messageList[0]]
    host = config["servers"][instructions["host"]]
    output, error = runRemote(log, instructions, host, messageList)
    if error == "":
      messageToSend = "Done\n"
      messageToSend += "Command output: " + str(output) + "\n"
      sendMessage(log, messageToSend)
    else:
      messageToSend = "Error\n"
      messageToSend += "Output: " + str(output) + "\n"
      messageToSend += "Error: " + str(error) + "\n"
      sendMessage(log, messageToSend)
  else:
    sendMessage(log, "Command not recognized")

  # Send known commands after each message
  sendKnownCommands(log)

@client.on(events.NewMessage(channelIdList))
async def main(event):
  # Update logger handler
  log = getLogger()
  receivedMessage = event.raw_text
  sender = str(event.from_id).split("=")[1].replace(")", "")
  if(sender not in botToken):
    # We do not want to process our messages
    log.info("Received new message: " + receivedMessage)
    processMessage(log, receivedMessage)

if __name__ == "__main__":
  # Create logger handler
  log = getLogger()

  client.start()
  log.info("Client started")

  sendMessage(log, "PiAsisstant restarted.")
  sendKnownCommands(log)

  client.run_until_disconnected()

