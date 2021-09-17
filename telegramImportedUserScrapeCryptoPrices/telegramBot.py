import json # for API response deserialization
import requests # for making API requests
import configparser # for reading config file
from telethon import TelegramClient, events # for interacting with Telegram

# Variables
api_id = 6879411
api_hash = '2dd2b314916470e49889845946162dd4'
path = "settings.ini"
apiEndpoint = "https://api.freshcoins.io/coins/slugs/"

# Get channel Id list
config = configparser.ConfigParser()
config.read(path)
channelIdList = [int(i) for i in config.sections()]

# Message template
template = (
       'Price {coinName} - ${coinSymbol} \n'
       '💸 <b>${price}</b>\n'
       'Marketcap \n'
       '🏦 <b>${marketCap} </b>\n'
       'Last 24h change \n'
       '📊 <b>{dailyChange}% </b>\n'
       ' \n'
       'Links related to ${coinSymbol} \n'
       '🔘 Check {coinName} <a href="{website}">Website</a> \n'
       '🔘 View chart <a href={viewLink}>here</a> \n'
       '🔘 Buy now from <a href="{buyLink}">here</a> \n'
       '🔘 View and VOTE ${coinSymbol} on <a href="{voteLink}">FreshCoins.io</a> \n'
)

def generateMessage(channelId):
  print('* Bot invoked in channel: ' + str(channelId) + '*')

  # Get info from config file
  config = configparser.ConfigParser()
  config.read(path)
  coinSlug = config.get(channelId, "coinslug")

  # Get data from freshcoins API
  response = requests.get(apiEndpoint + coinSlug)
  response = response.json()

  coinName = response["name"]
  coinSymbol = response["symbol"]
  price = response["price"]
  marketCap = str(int(response["marketcap"]))
  dailyChange = str('{:.2f}'.format(response["daily_change"]))
  website = response["website"]
  address = response["address"]
  network = response["network"]

  if network == "BSC":
    viewLink = "https://dextools.io/app/bsc/pair-explorer/" + address
    buyLink = "https://pancakeswap.finance/swap#/swap?outputCurrency=" + address
  elif network == "ETH":
    viewLink = "https://dextools.io/app/uniswap/pair-explorer/" + address
    buyLink = "https://app.uniswap.org/#/swap?outputCurrency=" + address
  elif network == "MATIC":
    viewLink = "https://dextools.io/app/polygon/pair-explorer/" + address
    buyLink = "https://app.sushi.com/swap?outputCurrency=" + address
  else:
    viewLink = "https://freshcoins.io"
    buyLink = "https://freshcoins.io"

  voteLink = "https://freshcoins.io/coins/" + coinSlug

  messageText = template.format(coinName=coinName, coinSymbol=coinSymbol, price=price, marketCap=marketCap, dailyChange=dailyChange,website=website, viewLink=viewLink, buyLink=buyLink, voteLink=voteLink)
  return messageText

print("Start client")
client = TelegramClient('bot', api_id, api_hash)
client.start()
print("Client started")

# Run bot
@client.on(events.NewMessage(channelIdList))
async def main(event):
  # print(event.raw_text.encode('utf-8'))
  if event.raw_text == '/price':
    await client.send_message(event.chat_id, message=generateMessage(str(abs(int(event.chat_id)))),parse_mode='html', link_preview=False)

print("Run bot")
client.run_until_disconnected()
