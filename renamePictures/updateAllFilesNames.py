import os
import re
from random import randint

# This small script is used when the other script identified
# wrongly the date of the pictures (date was not set on the camera)

dirPath = "D:\\Pictures\\2018 - 02 - Berlin"

year = "2018"
month = "02"
day = "11"

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def main():
  for root, subdirs, files in os.walk(dirPath):
    for file in files:
      if len(file.split(".")) > 1:
        ext = file.split(".")[-1]
      else:
        ext = "NOEXT"
      order = file[9:15]
      newName = str(year) + str(month) + str(day) + "_" + order + str(random_with_N_digits(5)) + "." + ext
      os.rename(os.path.join(root, file), os.path.join(root, newName))

if __name__ == "__main__":
  main()
