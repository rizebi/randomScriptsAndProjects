import os
import json
import time
import logging # for logging
import platform # to guess the host we are on
import datetime # for logging
import subprocess # for executing commands
from pathlib import Path # to read the password file
import urllib.request as request # to send messages
logging.getLogger('telethon').setLevel(logging.ERROR) # to avoid telethon log spam
from telethon import TelegramClient, events # to receive messages

# Read credentials
if "macOS" in platform.platform():
  tokenFolderPath = "/Users/eusebiurizescu/.telegram"
else:
  tokenFolderPath = "/root/Tools/Config"

currentDir = os.getcwd()
botToken = (Path(tokenFolderPath) / "telegramBotToken").read_text().replace("\\n", "").replace("\n", "")
apiId = (Path(tokenFolderPath) / "telegramApiId").read_text().replace("\\n", "").replace("\n", "")
apiHash = (Path(tokenFolderPath) / "telegramApiHash").read_text().replace("\\n", "").replace("\n", "")
channelIdList = [-442381868]
client = TelegramClient('bot', apiId, apiHash)

configFile = open("config.json")
config = json.load(configFile)

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
    output = output.decode('utf-8')
  except Exception as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e)  # to get the output even when error
  #log.info("Output: " + output)
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

def runLocal(log, instructions, messageList):
  pass

def runRemote(log, instructions, host, messageList):
  # Get password
  if "macOS" in platform.platform():
    sshPasswordText = Path("/Users/eusebiurizescu/.telegram/localnetflixPass").read_text().replace("\\n", "").replace("\n", "")
  else:
    sshPasswordText = Path(host["pass"]).read_text().replace("\\n", "").replace("\n", "")

  # Replace arguments in instructions command
  instructionsCommand = instructions["command"]
  for i in range(10):
    try:
      instructionsCommand = instructionsCommand.replace("$" + str(i), "\"" + messageList[i] + "\"")
    except:
      pass

  # Execute the command
  command = "sshpass -p '" + sshPasswordText + "' ssh -p " + host["port"] + " "+ host["user"] + "@" + host["ip"] + " " + instructionsCommand
  output, error = executeCommand(log, command)
  log.info("Output = " + str(output))
  log.info("Error = " + str(error))

  return str(error).replace(sshPasswordText, "SECRET")

def processMessage(log, receivedMessage):
  messageList = receivedMessage.split(" ")
  if messageList[0] in config["commands"].keys():
    instructions = config["commands"][messageList[0]]
    isLocal = config["servers"][instructions["host"]]["local"]
    if isLocal == "yes":
      error = runLocal(log, instructions, messageList)
    else:
      host = config["servers"][instructions["host"]]
      error = runRemote(log, instructions, host, messageList)
    if error == "":
      sendMessage(log, "Done")
    else:
      sendMessage(log, "Error: " + str(error))
  else:
    sendMessage(log, "Command not recognized")

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

  client.run_until_disconnected()
