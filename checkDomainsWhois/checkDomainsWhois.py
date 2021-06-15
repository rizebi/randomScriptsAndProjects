import os
import sys
import ssl # For ssl
import time # for sleep
import whois # for whois information
import socket # For ssl
import smtplib # for mail
import logging # for logging
import datetime # for logging
import traceback # for error handling
import subprocess # for executing bash

# pip3 install python-whois
# 0 12 * * * cd /root/checkDomainsWhois; /usr/bin/python3 checkDomainsWhois.py

## Variables
currentDir = os.getcwd()
domainsFile="domainsList.txt"
daysToExpireDomain = 30
daysToExpireSSL = 30
sleepSecondsBetweenQueries = 5 # Used in order to not get rate limiting by whois API
## Mail details
smtp_user = "REPLACE_SENDER_EMAIL"
smtp_pass = "REPLACE_SENDER_PASSWORD"
recipients = "REPLACE_RECEIVER_EMAIL"
smtp_server = "smtp.gmail.com"
scriptPurpose = "Check whois and ssl expiration for domains"

# Logging function
def getLogger():
  # Create logs folder if not exists
  if not os.path.isdir(os.path.join(currentDir, "logs")):
    try:
      os.mkdir(os.path.join(currentDir, "logs"))
    except OSError:
      print("Creation of the logs directory failed")
    else:
      print("Successfully created the logs directory")

  now = datetime.datetime.now()
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-checkDomainsWhois.log"
  log_name = os.path.join(currentDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Function that sends emails
def sendMail(log, status, summary, moreInfo):
  subject = "[" + status + "] "  + scriptPurpose
  msg = "Hello,\n\n"
  msg += "Task: " + scriptPurpose + "\n"
  msg += "General status: " + status + "\n\n"

  msg += "Summary:\n"
  msg += summary
  msg += "\n\nMore info:\n"
  if isinstance(moreInfo, str):
    msg += moreInfo
  else:
    msg += "Websites that are down:\n"
    msg += str(moreInfo["websitesDown"])
    msg += "\n\nDomains about to expire (domain name, remaining days):\n"
    msg += str(moreInfo["domainsToExpire"])
    msg += "\n\nSSL about to expire (domain name, remaining days):\n"
    msg += str(moreInfo["SSLToExpire"])
  msg += "\n\n"

  msg += "Best regards!\n"
  msg = ''.join([i if ord(i) < 128 else '_' for i in msg]) # Convert non ASCII characters
  sender = smtp_user
  message = "From: " + smtp_user + "\nSubject: {0}\n\n{1}".format(subject, msg)
  server = smtplib.SMTP_SSL(smtp_server, 465)
  server.ehlo()
  server.login(smtp_user, smtp_pass)
  server.sendmail(sender, recipients, message)
  server.close()
  log.info("Mail successfully sent")

# Function that read domains from the file
def readDomains(log):
  domainsList = open(os.path.join(currentDir, domainsFile), "r") # Read data
  domainsList = domainsList.read().split("\n")
  log.info(domainsList)
  # Remove spaces and cast to lowercase
  i = 0
  while i < len(domainsList):
    domainsList[i] = domainsList[i].strip().lower()
    domainsList[i] = domainsList[i].replace("https://", "")
    domainsList[i] = domainsList[i].replace("/", "")
    i += 1
  # Remove "\n" from list
  while "\n" in domainsList:
    domainsList.remove("\n")
  # Remove "" from list
  while "" in domainsList:
    domainsList.remove("")
  log.info(domainsList)
  return domainsList

# Function that checks if a domain is about to expire
def isDomainGoingToExpire(log, domain):
  log.info("Get expiration for domain: " + domain)
  try:
    w = whois.whois(domain)
  except Exception as e:
    log.info("Error when getting expiration date of domain")
    log.info(e)
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    return True, "CANNOT_GET_DATA"

  if type(w.expiration_date) == list:
    w.expiration_date = w.expiration_date[0]
  else:
    w.expiration_date = w.expiration_date

  now = datetime.datetime.now()
  timedelta = w.expiration_date - now
  days_to_expire = timedelta.days
  log.info("Domain remaining days: " + str(days_to_expire))

  if days_to_expire > daysToExpireDomain:
    return False, days_to_expire
  else:
    return True, days_to_expire


# Function that checks if SSL for a domain is about to expire
# Also, if we cannot get the SSL certificate, it means that the website is down
def isSSLGoingToExpire(log, domain):
  log.info("Get SSL for domain: " + domain)
  try:
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=domain,
    )
    # Set timeout for connection
    conn.settimeout(3.0)

    conn.connect((domain, 443))
    ssl_info = conn.getpeercert()
    expirationDate = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
    now = datetime.datetime.now()

    sslRemainingDays = (expirationDate - now).days
    log.info("SSL remaining days: " + str(sslRemainingDays))

    if sslRemainingDays > daysToExpireSSL:
      return True, False, sslRemainingDays
    else:
      return True, True, sslRemainingDays

  except Exception as e:
    log.info("Failed to get SSL: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    # Return isCurrentWebsiteUp = False, isCurrentSSLGoingToExpire = False (assume innocent, because we do not know the certificate)
    return False, False, -1

# Main function
def mainFunction():
  log = getLogger()
  log.info("################################# New run")

  try:
    # Read domains from file
    domainsList = readDomains(log)

    websitesDown = []
    domainsToExpire = []
    SSLToExpire = []

    # For each domain
    for domain in domainsList:
      log.info("######### Processing domain: " + domain)
      # Check it's current state
      isCurrentDomainGoingToExpire, remainingDomainDays = isDomainGoingToExpire(log, domain)
      isCurrentWebsiteUp, isCurrentSSLGoingToExpire, remainingSSLDays = isSSLGoingToExpire(log, domain)

      # Add to lists id the domain has problems (down, domain expire, ssl expire)
      if not isCurrentWebsiteUp:
        websitesDown.append(domain)
      if isCurrentDomainGoingToExpire:
        domainsToExpire.append([domain, remainingDomainDays])
      if isCurrentSSLGoingToExpire:
        SSLToExpire.append([domain, remainingSSLDays])

      # Sleep to avoid rate limiting
      log.info("Sleeping")
      time.sleep(sleepSecondsBetweenQueries)

    # Send mail
    if len(websitesDown) + len(domainsToExpire) + len(SSLToExpire) != 0:
      sendMail(log, "ACTION REQUIRED", "Action needed on some domains. See below.", {"websitesDown": websitesDown, "domainsToExpire": domainsToExpire, "SSLToExpire": SSLToExpire})
    else:
      # If it is monday, and all sites are good, send an email to ensure that script is running.
      if datetime.date.today().weekday() == 0:
        sendMail(log, "OK", "All good. This is just an email (sent only on Mondays to avoid spam), to ensure that the script is still running.", "Nothing to do. Relax :).")


  ##### END #####
  except KeyboardInterrupt:
    log.info("Quit")
    sys.exit(0)
  except Exception as e:
    log.info("Fatal Error: {}".format(e))
    tracebackError = traceback.format_exc()
    log.info(tracebackError)
    sendMail(log, "FATAL", str(e), str(tracebackError))
    sys.exit(98)


##### BODY #####
if __name__ == "__main__":

  if len(sys.argv) != 1:
    log.info("Wrong number of parameters. Use: python checkDomainsWhois.py")
    sys.exit(99)
  else:
    mainFunction()
