### Details
The script continuously send messages to Telegram groups. The message is composed randomly using many message chunks from message.txt

- The groups to send messages to, are read from file "groups.txt"
- The structure of groups.txt is:
   - 23235324, SPH   <- first is the chat id, then comma then coinName that you want to appear in the messages

### How to get chat id of a group?
Unfortunately you cannot get easily the chatId by Group Name. The best (almost automated) way I could find to get the chadId from Group Name, is that to run updateGroupMappings.py and a file "mappings.txt" will be created where the mappingsd between GroupNames and ChatIds will be written.
Run this script only when you need new chat ids. Do not abuse it (to not get ban)!


How exactly to get the mapping between group name and chat id?
Run "python3 updateGroupMappings.py", and the mapping between groupName and chatId will be written in "mapping.txt" file

### Prerequisites
- python3
- pip3
- Run: pip3 install telepot 

### How to get API keys
- Create Telegram application (to get api_id and api_hash). Go to http://my.telegram.org -> login with phone number and code received in the app -> API development tools -> Create new application -> Get api_id and api_hash

### How to configure the bot for the first time
- Make sure prerequisites are installed
- Create a folder with the code
- Update the parameters "api_id" and "api_hash" from both telegramBotSendMessageToGroups.py and updateGroupMappings.py with what you have created previously.
- Create file "message.txt" and enter there the message JSON (you can start from the example)
- Create file "groups.txt" and enter the chatIds and coinName, one per line. Leave empty if do not know the chatIds
- Run "python3 telegramBotSendMessageToGroups.py"
- It will ask for phone number. Add it (in format:  +4003453453425)
- The Telegram will send a code on application. Enter the code in the script
- Stop the bot
- Start it using: "bash start_bot.sh" in order to go in background
- Check file "mapping.txt" to see the mapping between the group and corresponding chat id
- Take the ID, and put it in groups.txt
- No need to restart the bot, it will always check the groups/message/image every run

### How to start the bot
- Just run: "bash start_bot.sh"

### How to add another group
- Add bot in the group
- Run "python3 updateGroupMappings.py" to update mapping.txt file. Take the chat id from there.
- Add chat id (do not ommit the "-" if present in mappings.txt) and add it in groups.txt: "23423423, SPH" for example
- No need to restart the bot