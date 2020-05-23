#!/usr/bin/python3

import sys
import time
import psutil
import smtplib
import datetime

smtp_user = "SENDER@gmail.com"
smtp_pass = "PASSWORD"
recipients = "RECEIVER@gmail.com"
smtp_server = "smtp.gmail.com"

def getUptime():
  return time.time() - psutil.boot_time()

def sendMail():
  print("Sending mail")
  now = str(datetime.datetime.now())
  subject = "[localnetflix] Do you still need me chief?"
  msg = "Hello chief,\n\n"
  msg += "I, localnetflix, I am still up\n"

  msg += "Best regards,\n"
  msg += "Your localnetflix"

  sender = "localnetflix"
  message = "From: localnetflix\nSubject: {0}\n\n{1}".format(subject, msg)

  server = smtplib.SMTP_SSL(smtp_server, 465)
  server.ehlo()
  server.login(smtp_user, smtp_pass)
  server.sendmail(sender, recipients, message)
  server.close()

try:
  if getUptime() >= 18000 and getUptime() <= 21600:
    sendMail()
  else:
   print("Not sending mail")

except:
  pass
