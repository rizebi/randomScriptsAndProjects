## Description
This is a Telegram bot that has a predefined list of commands. The commands are stored in config.json. The secrets are stored in secrets.env.gpg. It will be run with docker-compose, and the secrets from secrets.env.gpg will be decrypted and provided to the container as environment variables.
For example command: "startpersonal" will connect on host pi1 and will execute a specific command that will start a external hard drive

## How to run on local (for development) - no docker
# Stop production piAssistant
ssh pi1 sudo docker stop piassistant

# Do the dev
cd piAssistant
cat ~/Tools/Config/gpg | gpg -d --batch --yes --passphrase-fd 0 ./secrets.env.gpg > /tmp/secrets.env
sed -i -e 's/^/export /' /tmp/secrets.env
source /tmp/secrets.env
python3 piAssistant.py

# Start production piAssistant
ssh pi1 sudo docker start piassistant

## How to deploy on server - with docker
ssh pi1 sudo bash /root/Tools/homelab/utilities/refresh/main.sh piassistant

## TODO
- Make some commands "hidden" and to be shown only when running "/help"
