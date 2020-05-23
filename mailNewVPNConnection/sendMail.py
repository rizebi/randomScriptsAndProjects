import sys
import smtplib
import datetime


smtp_user = "carplannerroot@gmail.com"
smtp_pass = "samsungS3"
recipients = "rizescueusebiu@gmail.com"
smtp_server = "smtp.gmail.com"

try:
  now = str(datetime.datetime.now())
  subject = "New connection to home VPN"
  msg = "Hello chief,\n\n"
  msg += "New connection detected:\n"
  msg += "User: " + str(sys.argv[1]) + "\n"
  msg += "Public IP: " + str(sys.argv[2]) + "\n"
  msg += "Assigned IP: " + str(sys.argv[3]) + "\n"
  msg += "Timestamp: " + str(now) + "\n\n"
  msg += "Best regards,\n"
  msg += "Your humble Pi"

  sender = "OpenVPN Home"
  message = "From: OpenVPN Home\nSubject: {0}\n\n{1}".format(subject, msg)

  server = smtplib.SMTP_SSL(smtp_server, 465)
  server.ehlo()
  server.login(smtp_user, smtp_pass)
  server.sendmail(sender, recipients, message)
  server.close()
except:
  pass
