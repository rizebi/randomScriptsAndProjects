import os
import re
import time
import pytz
from PIL import Image
from random import randint
from datetime import datetime, timedelta
from win32com.propsys import propsys, pscon


# Requirements:
# pip install pillow, pywin32, pytz

# The final purpose of this script, is to get the taken date of a photo.
# and to rename the photo with the timestamp:
# 20160722_173949_52126.jpg YEARMONTHDAY_HOURMINSEC_RANDOM.EXT
# The best source from where to get this, is from date_taken metadata.
# But older photos and the WHATSAPP ones, do not have this metadata
# So we will establish the date from the following sources (in this order):
# 1) From date_taken medatada
# 2) If date_taken not present, will try media_created (as well metadata, but for videos)
# 3) If none present, we will try to get if from name
# 4) Lastly, From last modified. This is not safe, because for example if you rotate
#      a photo, last modified date will be updated


# NOTE
# Whatsapp on Apple does not name files in a way to extract at least the date
# So this script might get wrong date on photos from Whatsapp from Apple

startDir = "D:\\Pictures"


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def getLastModifiedDate(file):
  fileTime = os.path.getmtime(file)
  fileTime += 3*60*60
  return fileTime

def getDateTaken(file):
  try:
    im = Image.open(file)
    exif = im.getexif()
    fileTime = exif.get(36867)
    if fileTime is not None:
      if int(fileTime[0:4]) < 2000:
        return None
      datetime_object = datetime.strptime(fileTime, "%Y:%m:%d %H:%M:%S")
      epoch = datetime.utcfromtimestamp(0)
      return (datetime_object - epoch).total_seconds()
    else:
      return None
  except:
    #print("ERROR when get dateTaken from: " + file)
    return None

def getMediaDate(file):
  try:
    properties = propsys.SHGetPropertyStoreFromParsingName(file)
    dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
    if dt is None:
      return None
    if not isinstance(dt, datetime):
      dt = datetime.fromtimestamp(int(dt))
      dt = dt.replace(tzinfo=pytz.timezone('UTC'))

    dt_bucharest = dt.astimezone(pytz.timezone('Europe/Bucharest'))
    dt_bucharest = dt_bucharest.replace(tzinfo=None)
    epoch = datetime.utcfromtimestamp(0)
    fileTime = (dt_bucharest - epoch).total_seconds() + 2*60*60
    if fileTime < 946684800:
      return None
    return fileTime
  except:
    #print("ERROR when get mediaDate from: " + file)
    return None


def renameFile(root, file, fileTime, printNewName=False):
  year = str(time.gmtime(fileTime).tm_year)
  month = str('{:02d}'.format(time.gmtime(fileTime).tm_mon))
  day = str('{:02d}'.format(time.gmtime(fileTime).tm_mday))
  hour = str('{:02d}'.format(time.gmtime(fileTime).tm_hour))
  min = str('{:02d}'.format(time.gmtime(fileTime).tm_min))
  sec = str('{:02d}'.format(time.gmtime(fileTime).tm_sec))
  rand = str(random_with_N_digits(5))
  if len(file.split(".")) > 1:
    ext = file.split(".")[-1]
  else:
    ext = "NOEXT"
  newName = year + month + day + "_" + hour + min + sec + "_" + rand + "." + ext
  if(printNewName):
    print("newName = " + newName)

  #print("newName = " + newName)
  os.rename(os.path.join(root, file), os.path.join(root, newName))


def main():
  dateTakenFoundTotal = 0
  dateTakenNotFoundTotal = 0
  dateGotFromNameTotal = 0
  alreadyFormattedTotal = 0
  for root, subdirs, files in os.walk(startDir):
    #print("#########Processing directory = " + root)
    dateTakenFound = 0
    dateTakenNotFound = 0
    dateGotFromName = 0
    alreadyFormatted = 0
    for file in files:
      # print("Processing file = " + file)

      # 20160722_173949_52126.jpg
      # This is our custom format.
      # We MUST NOT remane a file already named by us. So skip
      alreadyFormattedBool = re.search("^[0-9]{8}_[0-9]{6}_[0-9]{5}\..*$", file)
      if alreadyFormattedBool:
        #print("Already formatted")
        alreadyFormatted += 1
        continue

      # First we are trying to take the date from "date_taken" metadata
      fileTime = getDateTaken(os.path.join(root, file))
      #print("dateTaken = " + str(fileTime))
      if fileTime is not None:
        renameFile(root, file, fileTime)
        dateTakenFound += 1
        continue

      # If date_taken not found, we will try to get it from Media Date (for videos)
      fileTime = getMediaDate(os.path.join(root, file))
      #print("dateTaken = " + str(fileTime))
      if fileTime is not None:
        renameFile(root, file, fileTime)
        dateTakenFound += 1
        continue

      #print("Nor DATE_TAKEN or MEDIA_DATE FOUND for file: " + os.path.join(root, file))
      dateTakenNotFound += 1

      # If the two above, fails, will try to get the date from name

      # Whatsapp: IMG-20160123-WA0003.jpeg  VID-20170105-WA0015.mp4   PTT-20190304-WA0000.opus     AUD-20190331-WA0006.opus
      if file.startswith("IMG-") or file.startswith("VID-") or file.startswith("PTT-") or file.startswith("AUD-"):
        # This means that it is a Whatsapp File (hopefully)
        try:
          year = int(file[4:8])
          month = int(file[8:10])
          day = int(file[10:12])
          pseudoSeconds = int(file[15:19])

          readTime = datetime(year, month, day)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds() + pseudoSeconds
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass


      # IMG_20141226_124658.jpg
      if file.startswith("IMG_"):
        try:
          year = int(file[4:8])
          month = int(file[8:10])
          day = int(file[10:12])
          hour = int(file[13:15])
          min = int(file[15:17])
          sec = int(file[17:19])

          readTime = datetime(year, month, day, hour, min, sec)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass



      #Screenshot_2014-10-28-15-26-39.png
      if file.startswith("Screenshot_"):
        try:
          year = int(file[11:15])
          month = int(file[16:18])
          day = int(file[19:21])
          hour = int(file[22:24])
          min = int(file[25:27])
          sec = int(file[28:30])

          readTime = datetime(year, month, day, hour, min, sec)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass


      # _20151115_210448.JPG
      if file.startswith("_"):
        try:
          year = int(file[1:5])
          month = int(file[5:7])
          day = int(file[7:9])
          hour = int(file[10:12])
          min = int(file[12:14])
          sec = int(file[14:16])

          readTime = datetime(year, month, day, hour, min, sec)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass


      #WP_20140829_001.mp4
      if file.startswith("WP_"):
        try:
          year = int(file[3:7])
          month = int(file[7:9])
          day = int(file[9:11])

          readTime = datetime(year, month, day)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass

      #P_20161019_103554_EFF.jpg
      if file.startswith("P_"):
        try:
          year = int(file[2:6])
          month = int(file[6:8])
          day = int(file[8:10])
          hour = int(file[11:13])
          min = int(file[13:15])
          sec = int(file[15:17])

          readTime = datetime(year, month, day, hour, min, sec)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass

      #PANO_20180212_105147.jpg
      if file.startswith("PANO_"):
        try:
          year = int(file[5:9])
          month = int(file[9:11])
          day = int(file[11:13])
          hour = int(file[14:16])
          min = int(file[16:18])
          sec = int(file[18:20])

          readTime = datetime(year, month, day, hour, min, sec)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass

      # 140830-1020.jpg  # This is an exception file
      if file.startswith("14"):
        try:
          year = int(file[0:2]) + 2000
          month = int(file[2:4])
          day = int(file[4:6])
          hour = int(file[7:9])
          min = int(file[9:11])

          readTime = datetime(year, month, day, hour, min)
          epoch = datetime.utcfromtimestamp(0)
          fileTimeSeconds = (readTime - epoch).total_seconds()
          renameFile(root, file, fileTimeSeconds)
          dateGotFromName += 1
          continue
        except:
          pass

      print("Nothing found for file: " + os.path.join(root, file))


      fileTime = getLastModifiedDate(os.path.join(root,file))
      renameFile(root, file, fileTime, printNewName=True)


    #print("dateTakenFound = " + str(dateTakenFound))
    #print("dateTakenNotFound = " + str(dateTakenNotFound))
    #print("dateGotFromName = " + str(dateGotFromName))
    dateTakenFoundTotal += dateTakenFound
    dateTakenNotFoundTotal += dateTakenNotFound
    dateGotFromNameTotal += dateGotFromName
    alreadyFormattedTotal += alreadyFormatted


  print("#######################")
  print("dateTakenFoundTotal = " + str(dateTakenFoundTotal))
  print("dateTakenNotFoundTotal = " + str(dateTakenNotFoundTotal))
  print("dateGotFromNameTotal = " + str(dateGotFromNameTotal))
  print("alreadyFormattedTotal = " + str(alreadyFormattedTotal))


if __name__ == "__main__":
  main()
