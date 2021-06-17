### Details

The script continuously send messages to Telegram groups, with configurable sleep time between messages.
- The text of message is read from file "message.txt" (can be changed to other file from "messageFile" variable from script)
- The groups to send messages to, are read from file "groups.txt" (can be changed to other file from "groupsFile" variable from script)
- The script has a default value of sleep between messages in script variable "defaultSleepMinutesBetweenMessages". This value can be changed for a specific group by adding in the groups.txt at the end of groupName ", X", and replace X with the number of minutes
- The structure of groups.txt is:
   - my_special_group, 4    <- first is the groupName, then comma then the interval in minutes between messages
   - my_other_group       <- the groupName, and the default interval between messages will be used
- To also send a picture with the message, add its path in "picturePath.txt" file (can be changed to other file from "pictureFile" variable from script)

### Prerequisites

- python3
- pip3
- Run: pip3 install telethon

### How to create a Telegram bot

Create bot (tutorial on the web, basically download app, search for user: BotFather, and use command /newbot), and keep the TOKEN
For example you can use this tutorial: https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot

### How to configure the bot for the first time

- Make sure prerequisites are installed
- Create a folder with the code
- Create file "message.txt" and enter there the message
- Create file "groups.txt" and enter the groupNames, one per line.
- Create file "picturePath.txt" and write there the path to image. Leave empty if no image should be sent
- Create Telegram application (to get api_id and api_hash). Go to http://my.telegram.org -> login with phone number and code received in the app -> API development tools -> Create new application -> Get api_id and api_hash
- Replace api_id and api_hash in the script
- Open CMD/Terminal, and go to the folder with the script (Run: cd path_to_script)
- Run the bot: python3 telegramUserSendMessageToGroups.py
- It will ask you for phone number and code received on the phone
- Change groups/messages/image without restarting the bot, it will always check the groups/message/image every run

### How to run the bot
- If the configurations did not change just run: python3 telegramBotSendMessageToGroups.py