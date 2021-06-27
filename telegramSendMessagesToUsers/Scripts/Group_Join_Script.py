from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors.rpcerrorlist import PeerFloodError
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.errors.rpcerrorlist import UserAlreadyParticipantError
from telethon.errors.rpcerrorlist import InviteHashInvalidError, InviteHashExpiredError, FloodWaitError
import random
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
phone = ''

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
    code = input("Enter the code: ")
    client.sign_in(phone, code)


groups_list_public = open("groups_public.txt", "r")
groups_list_private = open("group_list_private.txt", "r")

mode = int(input('Enter 1 for Public Groups, 2 for Private Group: '))

if mode == 1:
    for group in groups_list_public:
        try:
            group = group.strip('\n')
            client(JoinChannelRequest(group))
            print(f'Joined group {group.title()}')
            time.sleep(random.randrange(120, 180))

        except FloodWaitError:
            print('Flooding, Waiting for 1200 seconds!')
            time.sleep(1200)

        except PeerFloodError:
            print('Flood Error')
            client.disconnect()

        except:
            continue

elif mode == 2:
    for group in groups_list_private:
        try:
            group = group.strip('\n')
            client(ImportChatInviteRequest(group))
            print(f'Joined Private Group {group}')
            time.sleep(random.randrange(75, 120))

        except UserAlreadyParticipantError:
            print('User is Already Participant of that group!')
            continue

        except InviteHashInvalidError:
            print(f'{group} is expired!')
            continue

        except PeerFloodError:
            print('Flood Error')
            client.disconnect()


        except InviteHashExpiredError:
            print('Hash Expired')
            continue

        except FloodWaitError:
            print('Flooding, Waiting for 360 seconds!')
            time.sleep(360)
