### Details

The script continuously send messages to Telegram groups, with configurable sleep time between messages.
- The groups to send messages to, are read from file "groups.txt" (can be changed to other file from "groupsFile" variable from script). The format of the file is:
- my_special_group, 4, path_to_message, optional_path_to_image    <- first is the groupName, interval, path to message, optoonal path to image


### Prerequisites

- python3
- pip3
- Run: pip3 install telethon

### How to configure the bot for the first time

- Make sure prerequisites are installed
- Create a folder with the code
- Create folder "messages" and add message files there
- Create folder "pictures" and add pictures there
- Create file "groups.txt" and enter the groupNames, one per line.
- Create Telegram application (to get api_id and api_hash). Go to http://my.telegram.org -> login with phone number and code received in the app -> API development tools -> Create new application -> Get api_id and api_hash
- Replace api_id and api_hash in the script
- Open CMD/Terminal, and go to the folder with the script (Run: cd path_to_script)
- Run the bot: python3 telegramUserSendMessageToGroups.py
- It will ask you for phone number and code received on the phone
- Change groups/messages/image without restarting the bot, it will always check the groups/message/image every run

### How to run the bot
- If the configurations did not change just run: python3 telegramBotSendMessageToGroups.py