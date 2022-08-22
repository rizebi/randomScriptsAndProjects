import os
import json
import signal
import platform # to guess the host we are on
import urllib.request as request

from pathlib import Path # to read the password file
from datetime import datetime
from urllib.error import HTTPError
from http.client import HTTPResponse
from typing import Dict, List, Union

# Read token
if "macOS" in platform.platform():
  tokenFilePath = "/Users/eusebiurizescu/.telegram"
else:
  tokenFilePath = "/root/Tools/Config"
TOKEN = (Path(tokenFilePath) / "telegramToken").read_text().replace("\\n", "").replace("\n", "")

signal.signal(signal.SIGINT, signal.SIG_DFL)


class TelegramEcho:
  def __init__(self, TG_KEY: str):
    self.TG_URL = "https://api.telegram.org/bot{key}/{method}"
    self.TG_KEY = TG_KEY

    self.__last = None
    self.__last_time = None
    pass

  def run(self):
    """
    method to handle the incoming message and the send echo message to the user
    """
    while True:
      try:
        # getting the incoming data
        incoming = self.__handle_incoming()

        # checking if incoming message_id is same as of last, then skip
        if self.__last == incoming["message"]["message_id"]:
          continue
        else:
          self.__last = incoming["message"]["message_id"]

        # adding more validation to prevent messaging the last message whenever the polling starts
        if not self.__last_time:
          self.__last_time = incoming["message"]["date"]
          continue
        elif self.__last_time < incoming["message"]["date"]:
          self.__last_time = incoming["message"]["date"]
        else:
          continue

        # finally printing the incoming message
        self.__print_incoming(incoming)

        # now sending the echo message
        outgoing = self.__handle_outgoing(
          incoming["message"]["chat"]["id"],
          incoming["message"]["text"])

        # finally printing the outgoing message
        self.__print_outgoing(outgoing)

        pass
      except (HTTPError, IndexError):
        continue
      pass
    pass

  def __handle_incoming(self) -> Dict[str, Union[int, str]]:
    """
    method fetch the recent messages
    """

    # getting all messages
    getUpdates = request.urlopen(
      self.TG_URL.format(key=self.TG_KEY, method="getUpdates"))

    # parsing results
    results: List[Dict[str, Union[int, str]]] = json.loads(
      getUpdates.read().decode())["result"]

    # getting the last error
    return results[-1]

  def __print_incoming(self, incoming: Dict[str, Union[int, str]]):
    """
    method to print the incoming message on console
    """
    print("[<<<] Message Recieved on %s" % datetime.fromtimestamp(
      incoming["message"]["date"]).strftime("%Y-%m-%d %H:%M:%S"))
    print("\tText: %s" % incoming["message"]["text"])
    print("\tFrom: %s" %
        incoming["message"]["from"].get("first_name", "") + " " +
        incoming["message"]["from"].get("last_name", ""))
    print("\tMessage ID: %d" % incoming["message"]["message_id"])
    print("-" * os.get_terminal_size().columns)
    pass

  def __handle_outgoing(self, chat_id: int,
              message_txt: str) -> Dict[str, Union[int, str]]:
    """
    method to send the echo message to the same chat
    """

    # making the post data
    _data: Dict[str, Union[int, str]] = {
      "chat_id":
      chat_id,
      "text":
      "You sent me \"{MESSAGE_TEXT}\"".format(MESSAGE_TEXT=message_txt)
    }

    # creating the request
    _request: request.Request = request.Request(
      self.TG_URL.format(key=self.TG_KEY, method="sendMessage"),
      data=json.dumps(_data).encode('utf8'),
      headers={"Content-Type": "application/json"})

    # sending HTTP request, for sending message to the user
    sendMessage: HTTPResponse = request.urlopen(_request)
    result: Dict[str, Union[int, str]] = json.loads(
      sendMessage.read().decode())["result"]
    return result

  def __print_outgoing(self, outgoing):
    """
    method to print outgoing data on the console
    """
    print("[>>>] Message Send on %s" % datetime.fromtimestamp(
      outgoing["date"]).strftime("%Y-%m-%d %H:%M:%S"))
    print("\tText: %s" % outgoing["text"])
    print("\tFrom: %s" % outgoing["from"]["first_name"])
    print("\tMessage ID: %d" % outgoing["message_id"])
    print("-" * os.get_terminal_size().columns)
    pass

  pass


if __name__ == "__main__":
  tg = TelegramEcho(TOKEN)
  tg.run()