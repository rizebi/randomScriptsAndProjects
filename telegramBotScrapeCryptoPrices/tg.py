from telethon import TelegramClient, events
import undetected_chromedriver.v2 as uc
import time
import configparser

from bs4 import BeautifulSoup
api_id = REPLACE
api_hash = 'REPLACE'
bot_token = ''

channelIdList = [553270668, 521440549, 561526530, 572171595, 597032167]
path = "settings.ini"
client = TelegramClient('bot', api_id, api_hash)

client.start()
print("Client started")



template = (
       'Price {coinName} - ${coinShortName} \n'
       '💸 <b>{price}</b>\n'
       'Marketcap \n'
       '🏦 <b>{marketCap} </b>\n'
       ' \n'
       'Links related to ${coinShortName} \n'
       '🔘 Check {coinName} <a href="{link1}">Website</a> \n'
       '🔘 View chart on <a href=poocoin.app/tokens/{address}>Poocoin</a> \n'
       '🔘 View chart on <a href="charts.bogged.finance/?token={address}">Bogged.Finance</a> \n'
       '🔘 Buy now on <a href="exchange.pancakeswap.finance/#/swap?outputCurrency={address}">PancakeSwap</a> \n'
       '🔘 View and VOTE ${coinShortName} on <a href="{link2}">FreshCoins.io</a> \n'
)








config = configparser.ConfigParser()
config.read(path)


def genMessage(channelId):
    print('*'+channelId+'*')
    config = configparser.ConfigParser()
    config.read(path)    
    price  = config.get(channelId, "price")
    coinName = config.get(channelId, "coinName")
    coinShortName = config.get(channelId, "coinShortName")
    link1 = config.get(channelId, "link1")
    link2 = config.get(channelId, "link2")
    address = config.get(channelId, "address")
    marketCap= config.get(channelId, "marketCap")
    str = template.format(coinName=coinName, coinShortName=coinShortName,price=price,marketCap=marketCap,link1=link1,link2=link2,address=address) 
    print(str)
    return str




@client.on(events.NewMessage(channelIdList))
async def main(event):
     print(event.raw_text)
     if event.raw_text == '/price':
         await client.send_message(event.chat_id, message=genMessage(str(abs(int(event.chat_id)))),parse_mode='html', link_preview=False)

client.run_until_disconnected()
