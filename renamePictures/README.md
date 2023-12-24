## Currently scripts runs on Windows only

The purpose of main script, named renameFilesByDate.py, is to get the taken date of a photo and to RENAME the photo with that timestamp loke below:
20160722_173949_52126.jpg YEARMONTHDAY_HOURMINSEC_RANDOM.EXT

Now the question is, where is the best place to take this date from? File created? Filed last modified? Other metadata?

The best source from where to get this, is from date_taken metadata, but some older photos and the WHATSAPP ones, do not have this metadata.

So we will establish the date from the following sources (in this order):
1) From date_taken medatada
2) If date_taken not present, will try media_created (as well metadata, but for videos)
3) If none present, we will try to get if from name
4) Lastly, From last modified. This is not safe, because for example if you rotate
   a photo, last modified date will be updated

Use of this script:
1) Change variable startDir from file with the directory where you want to apply
2) Run: python3 renameFilesByDate.py

#################################################################

The purpose of the other script, updateAllFilesNames.py, is to use it when the above script did not identified correctly the dates. (for example, on older cameras the date was not already set, and you can and up with a folder with 500 pictures fom 1-Jan-2006)

Use of this script:
1) Set dirPath, year, month and day variables
2) Run python3 updateAllFilesNames.py

#################################################################

Flow when want to add new pictures / videos to existing collection:

1) Delete all .AAE files (these are some files from iPhones created when editing photos)
2) Run dupeGuru, in "Content" way to delete all 100% identicals
3) Run dupeGuru, in "Pictures" way, with index 96% to delete duplicate pictures
   (96% is good to detect similar between Whatsapp and Camera)
4) Run VideoDuplicateFinder, with index 99% to delete Video duplicates (.MOV files form Iphone)
5) Run renameFilesByDate.py to rename the pictures/videos.
6) Merge pictures

#################################################################

Above mentioned programs:
1) https://dupeguru.voltaicideas.net/
2) https://github.com/0x90d/videoduplicatefinder
