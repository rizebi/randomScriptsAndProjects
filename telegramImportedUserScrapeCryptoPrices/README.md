Pentru a adauga un nou canal, trebuie adaugat botul in noul canal si apoi trebuie rulat:
python3 getChannelID.py
Apoi trebuie luat channel id (daca are "-" in fata trebuie ignorat. Merge si fara), si pus in settings.ini.
In settings.ini merge copiat de la altul deja existent, si inlocuit ce difera (adresa, cahnnel_id, etc.)
Apoi trebuie oprite procesele:
./stop_processes.sh
Si apoi repornite:
./start_processes.sh
