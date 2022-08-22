import os
import sys
import json # for JSON manipulation
import logging # for logging
import datetime # for logging and parsing dates
import traceback # for error handling
import matplotlib.pyplot as plt

##### Variables #####
statementsFolder = "/Users/eusebiurizescu/Downloads/extrase"

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
def processTransaction(log, balanceDict, transaction, fileName):

  fileName = fileName.split("/")[-1]

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
  transaction[-2] = transaction[-2].replace(".", "").replace(",", ".")
  transaction = "".join(transaction)
  transaction = replaceMonths(log, transaction)
  transaction = transaction.split(',')

  #log.info(transaction)

  transactionTimestamp = int(datetime.datetime.strptime(transaction[0], '%d %B %Y').strftime("%s"))

  balance = float(transaction[-1])
  if "EUR" in fileName:
    balance *= eurToRonMediumExchangeRate

  if transactionTimestamp not in balanceDict:
    balanceDict[transactionTimestamp] = {}
    balanceDict[transactionTimestamp][fileName] = balance
  else:
    if fileName not in balanceDict[transactionTimestamp]:
      balanceDict[transactionTimestamp][fileName] = balance

# Function that process one file
# balanceDict is a dictionary for the transactions
def processStatement(log, balanceDict, fileName):

  transactions = open(fileName, "r")
  transactions = transactions.read().split("\n")

  for transaction in transactions:
    processTransaction(log, balanceDict, transaction, fileName)

# This function get the dictionary with all the balances
# and will generate datapoints
# {"<date>": {"<filename>": 234}}
def generateDataPoints(log, balanceDict):

  fileList = os.listdir(statementsFolder)
  latestBalanceForEachAccountDict = {}
  for file in fileList:
    latestBalanceForEachAccountDict[file] = 0

  dateList = []
  for key in balanceDict.keys():
    dateList.append(key)
  dateList.sort()

  balanceList = []

  for iterDate in dateList:
    # log.info("##### Date: " + str(datetime.datetime.fromtimestamp(int(iterDate))))
    currentBalance = 0
    fileList = os.listdir(statementsFolder)
    # For each file in the day balances
    for file in balanceDict[iterDate].keys():
      # log.info("For file: " + file + " got: " + str(balanceDict[iterDate][file]))
      currentBalance += balanceDict[iterDate][file]
      latestBalanceForEachAccountDict[file] = balanceDict[iterDate][file]
      fileList.remove(file)

    # For the files that on this date do not have any balances listed, take the last known balance
    for file in fileList:
      currentBalance += latestBalanceForEachAccountDict[file]
      # log.info("For file: " + file + " got from memory: " + str(latestBalanceForEachAccountDict[file]))

    balanceList.append(currentBalance)

  return [dateList, balanceList]

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
def mainFunction():
  # Initialize the logger
  log = getLogger()
  log.info("############################################# New run of script")

  try:
    if not os.path.isdir(statementsFolder):
      log.info("statementsFolder = " + statementsFolder + " not found.")
      sys.exit(1)

    balanceDict = {}

    for statementFile in os.listdir(statementsFolder):
      f = os.path.join(statementsFolder, statementFile)
      # checking if it is a file
      if os.path.isfile(f):
        log.info("Processing file " + f)
        processStatement(log, balanceDict, f)

    # Generate datapoints from dict
    dataPoints = generateDataPoints(log, balanceDict)

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

  if len(sys.argv) != 1:
    log = getLogger()
    log.info("Wrong number of parameters. Use: python bankBalanceGraphMaker.py")
    sys.exit(100)
  else:
    mainFunction()
