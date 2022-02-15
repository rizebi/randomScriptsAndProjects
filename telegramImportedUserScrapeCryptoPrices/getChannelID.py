from telethon import TelegramClient,sync

api_id = 111111
api_hash = '111111111111111111111111111'
client = TelegramClient('bot', api_id, api_hash)

client.start()
for chat in client.get_dialogs():
    print('name:{0} ids:{1} is_user:{2} is_channel{3} is_group:{4}'.format(chat.name,chat.id,chat.is_user,chat.is_channel,chat.is_group).encode('utf-8'))
