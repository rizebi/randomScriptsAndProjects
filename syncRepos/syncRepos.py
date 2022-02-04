import os
import sys
import json # for JSON manipulation
import shutil # delete folder
import logging # for logging
import datetime # for logging and parsing dates
import traceback # for error handling
import subprocess # for executing bash

##### Variables #####
localFolderPath = "C:\\tmp"
sourceRepoPath = "git@github.com:rizebi/randomScriptsAndProjects.git"
destinationRepoPath = "git@github.com:rizebi/destination.git"

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
  log_name = "" + str(now.year) + "." + '{:02d}'.format(now.month) + "." + '{:02d}'.format(now.day) + "-syncRepos.log"
  log_name = os.path.join(baseDir, "logs", log_name)
  logging.basicConfig(format='%(asctime)s  %(message)s', level=logging.NOTSET,
                      handlers=[
                      logging.FileHandler(log_name),
                      logging.StreamHandler()
                      ])
  log = logging.getLogger()
  return log

def executeCommand(command):
  error = ""
  output = ""
  print("Executing: " + command)
  try:
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
  except subprocess.CalledProcessError as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e.output).replace("\\n", "\n")  # to get the output even when error
  except Exception as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e)  # to get the output even when error
  #print("Output: " + output)
  return output, error

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    # Is the error an access error?
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

# Main function
def mainFunction():
  # Initialize the logger
  log = getLogger()
  log.info("############################################# New run of script")
  global localFolderPath

  try:
    log.info("Make sure the localFolderPath exists")
    if not os.path.isdir(localFolderPath):
      log.info("localFolderPath does not exist. Exiting.")
      sys.exit(1)
    log.info("Folder exists, all good. Continuing.")

    localFolderPath = os.path.join(localFolderPath, "tmp")
    log.info("Delete " + localFolderPath + " folder")
    try:
      shutil.rmtree(localFolderPath, onerror=onerror)
    except:
      pass
    log.info("Successfully deleted")

    log.info("Create new 'tmp' folder in provided folder")
    os.mkdir(localFolderPath)

    log.info("Clone source repo in: " + localFolderPath)
    command = "cd " + localFolderPath + "& git clone " + sourceRepoPath + " ."
    output, error = executeCommand(command)
    log.info("Output: " + output)
    if error != "":
      log.info("ERROR when cloning source repo:")
      log.info(error)
      sys.exit(2)

    log.info("Rename origin to upstream")
    command = "cd " + localFolderPath + "& git remote rename origin upstream"
    output, error = executeCommand(command)
    log.info("Output: " + output)
    if error != "":
      log.info("ERROR when renaming origin to upstream:")
      log.info(error)
      sys.exit(3)

    log.info("Add destination repository as origin")
    command = "cd " + localFolderPath + "& git remote add origin " + destinationRepoPath
    output, error = executeCommand(command)
    log.info("Output: " + output)
    if error != "":
      log.info("ERROR when adding destination repository as origin:")
      log.info(error)
      sys.exit(4)

    log.info("Push to destination")
    command = "cd " + localFolderPath + "& git push origin master"
    output, error = executeCommand(command)
    log.info("Output: " + output)
    if error != "":
      log.info("ERROR when pushing to destination:")
      log.info(error)
      sys.exit(4)



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
    log.info("Wrong number of parameters. Use: python syncRepos.py")
    sys.exit(100)
  else:
    mainFunction()
