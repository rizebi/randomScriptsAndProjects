Script that send mail if the server was started more than 5 hours ago.
Also, if it was started more than 6 hours ago, the script will not spam.

Crontab needed:
0 * * * * /usr/local/bin/sendMailUptime.py
