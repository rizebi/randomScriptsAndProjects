import os
import sys
import json # for JSON manipulation
import logging # for logging
import datetime # for logging and parsing dates
import traceback # for error handling
import matplotlib.pyplot as plt

##### Variables #####
statementsFolder = "/Users/eusebiu.rizescu/Downloads/extrase"

eurToRonMediumExchangeRate = 4.9204 # For 2021

##### Functions #####

# Logging function
def getLogger():
  baseDir = os.getcwd()
  # Create logs folder if not exists
  if not os.path.isdir(os.path.join(baseDir, "logs")):
    try:
      os.mkdir(os.path.join(baseDir, "logs"))
    except OSError:
      print("Creation of the logs directory failed")
    else:
      print("Successfully created the logs directory")

  now = datetime.datetime.now()
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-bankBalanceGraphMaker.log"
  log_name = os.path.join(baseDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

# Replace month name from Romanian to English
def replaceMonths(log, transaction):

  transaction = transaction.replace("ianuarie", "january")
  transaction = transaction.replace("februarie", "february")
  transaction = transaction.replace("martie", "march")
  transaction = transaction.replace("aprilie", "april")
  transaction = transaction.replace("mai", "may")
  transaction = transaction.replace("iunie", "june")
  transaction = transaction.replace("iulie", "july")
  transaction = transaction.replace("august", "august")
  transaction = transaction.replace("septembrie", "september")
  transaction = transaction.replace("octombrie", "october")
  transaction = transaction.replace("noiembrie", "november")
  transaction = transaction.replace("decembrie", "december")

  return transaction

# Function that sanitize and process one transaction
def processTransaction(log, transactionsDict, transaction, fileName):

  # Check if line contains a transaction
  months = ["ianuarie", "februarie", "martie", "aprilie", "mai", "iunie", "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"]

  res = [ele for ele in months if(ele in transaction)]

  # The line does not contain a valid transaction
  if len(res) == 0:
    return
  # Hack to treat case when description of the transaction contains name of one month
  if "Detalii:" in transaction:
    return

  transaction = transaction.split('"')
  transaction[1] = transaction[1].replace(".", "").replace(",", ".")
  transaction = "".join(transaction)
  transaction = replaceMonths(log, transaction)
  transaction = transaction.split(',')

  log.info(transaction)

  transactionTimestamp = int(datetime.datetime.strptime(transaction[0], '%d %B %Y').strftime("%s"))
  if transaction[6] != "":
    amount = (-1) * float(transaction[6])
  else:
    try:
      amount = float(transaction[8])
    except:
      # Hack because CSV file from bank is junk
      amount = float(transaction[7])

  if "EUR" in fileName:
    amount *= eurToRonMediumExchangeRate

  if transactionTimestamp not in transactionsDict:
    transactionsDict[transactionTimestamp] = amount
  else:
    transactionsDict[transactionTimestamp] += amount


# Function that process one file
# transactionsDict is a dictionary for the transactions
def processStatement(log, transactionsDict, fileName):

  transactions = open(fileName, "r")
  transactions = transactions.read().split("\n")

  for transaction in transactions:
    processTransaction(log, transactionsDict, transaction, fileName)

# This function get the dictionary with all the transaction, and current balance
# And will generate datapoints
def generateDataPoints(log, transactionsDict, currentBalance):

  intermediaryList = []
  for key in transactionsDict.keys():
    intermediaryList.append([key, transactionsDict[key]])

  intermediaryList.sort(key=lambda x:x[0], reverse=True)

  # Now we have the transaction list sorted reversely
  dataPointsX = []
  dataPointsY = []
  for element in intermediaryList:
    dataPointsX.append(element[0])
    dataPointsY.append(currentBalance - element[1])
    currentBalance -= element[1]

  dataPointsX.reverse()
  dataPointsY.reverse()
  
  return [dataPointsX, dataPointsY]

def plot(log, dataPoints):

  dataPointsX = dataPoints[0]
  dataPointsY = dataPoints[1]

  dataPointsTmp = []
  for elem in dataPointsX:
    dataPointsTmp.append(datetime.datetime.fromtimestamp(int(elem)))

  dataPointsX = dataPointsTmp

  #Create the Python figure
  #Set the size of the matplotlib canvas
  fig = plt.figure(figsize = (18,8))

  # Details
  plt.title("Bank Account Balance History")
  plt.ylabel("Balance")
  plt.xlabel("Date")

  # Show axes in both sides
  ax = fig.add_subplot(111)
  ax.yaxis.tick_right() # This breaks for manual plot, but for API it puts ok the scale on the right
  ax.yaxis.set_ticks_position('both')
  ax.tick_params(labeltop=False, labelright=True)

  # Show grid
  plt.grid(color='grey', linestyle='-', linewidth=0.3)

  # Plot prices
  plt.plot(dataPointsX, dataPointsY, linewidth=3)

  # Show plot
  plt.show()


# Main function
def mainFunction(currentBalance):
  # Initialize the logger
  log = getLogger()
  log.info("############################################# New run of script")
  log.info("Current Balance: " + str(currentBalance))

  try:
    if not os.path.isdir(statementsFolder):
      log.info("statementsFolder = " + statementsFolder + " not found.")
      sys.exit(1)

    transactionsDict = {}

    for statementFile in os.listdir(statementsFolder):
      f = os.path.join(statementsFolder, statementFile)
      # checking if it is a file
      if os.path.isfile(f):
        log.info("Processing file " + f)
        processStatement(log, transactionsDict, f)

    # Generate datapoints from dict
    dataPoints = generateDataPoints(log, transactionsDict, currentBalance)

    # Plot
    plot(log, dataPoints)

  ##### END #####
  except KeyboardInterrupt:
      log.info("Quit")
      sys.exit(0)
  except Exception as e:
      log.info("FATAL ERROR: {}".format(e))
      tracebackError = traceback.format_exc()
      log.info(tracebackError)
      sys.exit(99)


##### BODY #####
if __name__ == "__main__":

  if len(sys.argv) != 2:
    log = getLogger()
    log.info("Wrong number of parameters. Use: python bankBalanceGraphMaker.py <currentBalance>")
    sys.exit(100)
  else:
    currentBalance = sys.argv[1]
    mainFunction(float(currentBalance))
