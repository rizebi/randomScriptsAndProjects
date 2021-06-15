### How to use

#### Prerequisites
- Install python3
- Install pip
- pip3 install python-whois

#### Configure
- Add domains in file a file named "domainsList.txt", next to file checkDomainsWhois.py
- Change adjust in the code "daysToExpireDomain" and "daysToExpireSSL" in order to change when to be notified. Default is 30 days
- Change "smtp_user"/"smtp_pass"/"smtp_server" if they are changed. At the moment of this writing, a new gmail account is used as a sender email address
- Change "recipients" with the email that should receive the notifications
- Run: python3 checkDomainsWhois.py
- Add crontab: 0 12 * * * cd /root/checkDomainsWhois; /usr/bin/python3 checkDomainsWhois.py