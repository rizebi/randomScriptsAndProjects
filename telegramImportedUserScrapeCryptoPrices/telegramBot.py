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
       '💸 <b>{price}</b>\n'
       'Marketcap \n'
       '🏦 <b>{marketCap} </b>\n'
       'Last 24h change \n'
       '📊 <b>{dailyChange}% </b>\n'
       ' \n'
       'Links related to ${coinSymbol} \n'
       '🔘 Check {coinName} <a href="{link1}">Website</a> \n'
       '🔘 View chart on <a href=poocoin.app/tokens/{address}>Poocoin</a> \n'
       '🔘 View chart on <a href="charts.bogged.finance/?token={address}">Bogged.Finance</a> \n'
       '🔘 Buy now on <a href="exchange.pancakeswap.finance/#/swap?outputCurrency={address}">PancakeSwap</a> \n'
       '🔘 View and VOTE ${coinSymbol} on <a href="{link2}">FreshCoins.io</a> \n'
)

def generateMessage(channelId):
  print('* Bot invoked in channel: ' + str(channelId) + '*')
  config = configparser.ConfigParser()
  config.read(path)

  slugInApi = config.get(channelId, "sluginapi")
  link1 = config.get(channelId, "link1")
  link2 = config.get(channelId, "link2")

  # Get data from freshcoins API
  response = requests.get(apiEndpoint + slugInApi)
  response = response.json()

  coinName = response["name"]
  coinSymbol = response["symbol"]
  price = response["price"]
  address = response["address"]
  marketCap = str('{:.2f}'.format(response["marketcap"]))
  dailyChange = str('{:.2f}'.format(response["daily_change"]))

  messageText = template.format(coinName=coinName, coinSymbol=coinSymbol,price=price,marketCap=marketCap,dailyChange=dailyChange,link1=link1,link2=link2,address=address)
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
