mkdir /mailOpenVPN

chmod 777 /mailOpenVPN

vim /mailOpenVPN/sendMail.py

vim /etc/openvpn/up.sh
#! /bin/sh
python3 /mailOpenVPN/sendMail.py $X509_0_CN $trusted_ip $ifconfig_pool_remote_ip

chmod +x /etc/openvpn/up.sh

vim /etc/openvpn/server.conf
script-security 2
client-connect /etc/openvpn/up.sh

service openvpn restart


https://askubuntu.com/questions/28733/how-do-i-run-a-script-after-openvpn-has-connected-successfully/1225138#1225138
