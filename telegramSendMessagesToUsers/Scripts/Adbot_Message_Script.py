from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import ChatWriteForbiddenError, SlowModeWaitError, UserBannedInChannelError, ChannelPrivateError, FloodWaitError, ChatRestrictedError
import time
import proxy_utils

proxy_host = ""
proxy_port = 0
proxy_type = "http"
proxy_user = ""
proxy_password = ""

USE_PROXY = True
api_id = 
api_hash = '' 
phone = '+'    

if USE_PROXY:
    px_session = str(phone) + str(api_id) + str(api_hash)
    proxy = proxy_utils.get_session_proxy(px_session)
    if not proxy:
        try:
            proxy = proxy_utils.create_proxy(proxy_type,proxy_host,proxy_port,proxy_user,proxy_password)
        except NameError:
            print("Error: the proxy of this account is not saved, please add the proxy variables")
        finally:
            proxy_utils.save_session_proxy(px_session, proxy)
    client = TelegramClient(phone, api_id, api_hash, proxy=proxy)
else:
    client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
groups = []
chunk_size = 200
last_date = None

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except:
        continue

market_groups = []

for g in groups:
    market_groups.append(g.id)


message = '''

AD MSG
HERE


'''

x = 0
y = len(market_groups)
z = 1

while z == 1:
    for i in range(y):
        try:
            client.send_message(market_groups[i], message)
            time.sleep(25) # Time Gap After Sending message to one group

        except ChatWriteForbiddenError:
            time.sleep(15)

        except SlowModeWaitError:
            time.sleep(30)

        except ChatRestrictedError:
            time.sleep(30)

        except ChannelPrivateError:
            time.sleep(90)

        except UserBannedInChannelError:
            print('Account Limited')
            time.sleep(7200)

        except FloodWaitError:
            time.sleep(450)

    print('Message Sent To All Groups!')
    time.sleep(3600) #  Time-Gap for Sendig Whole Message to All Groups!

client.start()
