Conectare masina:
ssh -i fisier centos@18.188.184.27

Dupa ce te loghezi dai "sudo su"
Pentru a adauga un nou canal, trebuie adaugat botul in noul canal si apoi trebuie rulat:
python3 getChannelID.py
Apoi trebuie luat channel id (daca are "-" in fata trebuie ignorat. Merge si fara), si pus in settings.ini.
In settings.ini merge copiat de la altul deja existent, si inlocuit ce difera (adresa, cahnnel_id, etc.)
Acelasi channel id trebuie pus si in tg.py, in parametrul channelIdList. Trebuie doar pus virgula la final, si pus channel id acolo.
Apoi trebuie oprite procesele:
./stop_processes.sh
Si apoi repornite:
./start_processes.sh
