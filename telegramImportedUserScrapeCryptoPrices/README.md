## Adaugare canal bot

1) Adaugat userul de telegram in noul canal
2) Conectat server
ssh root@api.freshcoins.io
3) sudo su
4) cd /scripts/telegramBotCryptoPrices
5) Trebuie gasit ID-ul noului canal. Ruleaza: python3 getChannelID.py
Si luat id-ul din ce returneaza programul
6) Restartat botul:
./stop_bot.sh
Si apoi repornite:
./start_bot.sh
