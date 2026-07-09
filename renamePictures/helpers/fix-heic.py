import os
import re
import time
from random import randint
from win32com.propsys import propsys, pscon

# Requirements:
# pip install pywin32

# Renames only HEIC files using Windows "Date Taken" metadata.
# Naming format:
# YYYYMMDD_HHMMSS_RANDOM.HEIC

startDir = "Z:\\Poze"

# Set to False to actually rename files
dryRun = False


def random_with_N_digits(n):
  range_start = 10 ** (n - 1)
  range_end = (10 ** n) - 1
  return randint(range_start, range_end)


def getDateTaken(file):
  print(file)
  try:
    properties = propsys.SHGetPropertyStoreFromParsingName(file)
    dt = properties.GetValue(pscon.PKEY_Photo_DateTaken).GetValue()

    print("DateTaken =", dt)

    if dt is None:
      return None

    return dt.timestamp()

  except Exception:
    import traceback
    traceback.print_exc()
    return None


def renameFile(root, file, fileTime):
  t = time.localtime(fileTime)

  year = f"{t.tm_year:04d}"
  month = f"{t.tm_mon:02d}"
  day = f"{t.tm_mday:02d}"
  hour = f"{t.tm_hour:02d}"
  minute = f"{t.tm_min:02d}"
  second = f"{t.tm_sec:02d}"

  rand = random_with_N_digits(5)

  ext = file.split(".")[-1]
  newName = f"{year}{month}{day}_{hour}{minute}{second}_{rand}.{ext}"

  # If only the random part differs, don't rename.
  oldBase = re.sub(r"_\d{5}(\.[^.]+)$", r"\1", file, flags=re.IGNORECASE)
  newBase = re.sub(r"_\d{5}(\.[^.]+)$", r"\1", newName, flags=re.IGNORECASE)

  if oldBase.lower() == newBase.lower():
    print(f"Skipping (same timestamp): {file}\n")
    return False

  oldPath = os.path.join(root, file)
  newPath = os.path.join(root, newName)

  print(f"Old: {file}")
  print(f"New: {newName}")

  if dryRun:
    print("DRY RUN - Not renamed\n")
  else:
    os.rename(oldPath, newPath)
    print("Renamed\n")

  return True


def main():
  renamed = 0
  notFound = 0

  for root, _, files in os.walk(startDir):
    for file in files:

      # Only process HEIC files
      if not file.lower().endswith(".heic"):
        continue

      fileTime = getDateTaken(os.path.join(root, file))

      if fileTime is None:
        print("No Date Taken:", os.path.join(root, file))
        notFound += 1
        continue

      renameFile(root, file, fileTime)
      renamed += 1

  print("#######################")
  print(f"Dry Run       : {dryRun}")
  print(f"Renamed       : {renamed}")
  print(f"No Date Taken : {notFound}")


if __name__ == "__main__":
  main()