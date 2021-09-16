import traceback # for error handling
import configparser
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver # for scraping
from selenium.webdriver.chrome.options import Options
import subprocess # for executing bash

path = "settings.ini"

def executeCommand(command):
  error = ""
  output = ""
  print("Executing: " + command)
  try:
    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    output = output.decode('utf-8')
  except Exception as e:
    error = "ERROR: " + str(e.returncode) + "  " + str(e) + "\n"
    output = repr(e)  # to get the output even when error
  #print("Output: " + output)
  return output, error



while 1<2:

    config = configparser.ConfigParser()
    config.read(path)


    for section in config.sections():
        address = config.get(section, "address")
        print("###### Kill older processes of chromedriver and xvfb")
        output, error = executeCommand('kill -kill $(ps -eaf | grep -i chrome | grep -v grep | tr -s " " | cut -d " " -f 2)')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36")
        driver = webdriver.Chrome(chrome_options=chrome_options)

        try:     
            print ('https://charts.bogged.finance/?token=' + address)
            driver.get('https://charts.bogged.finance/?token=' + address)  # known url using cloudflare's "under attack mode"
            print ("Sleeping 10 sec for page to load")
            time.sleep (10)
            #driver.save_screenshot('poocoin.png')
            content = driver.page_source
            #print ("CONTENT:")
            #print (content)
            #print ("End content")
            soup = BeautifulSoup(content, features="html.parser")
            try:
              divMarketCap = soup.findAll('div', attrs={'class':'items-center lg:h-16 h-10 lg:bg-transparent bg-white dark:bg-transparent flex flex-row justify-center text-center lg:text-left lg:justify-start space-x-3 lg:pt-0 lg:my-1.5 my-0 sm:space-x-6 w-full lg:w-auto'})
              for span in divMarketCap[0].findAll('span'):
                  if "Marketcap" in str(span) and "$" in str(span):
                      marketcap = span.findAll('h4')[0].text.strip()
            except:
              marketcap = 0

            try:
              price = "$" + str(soup.findAll('title')).split("$")[1].split(" ")[0]
            except:
              price = 0

            try:
              divsIndex = soup.findAll('div', attrs={'flex flex-row space-x-2 items-center'})
              for divIndex in divsIndex:
                for h4 in divIndex.findAll('h4'):
                    if "%" in str(h4):
                      index = h4.text.strip().replace("%", "")
            except:
              index = 0

            print(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            string = 'Market Cap= '+marketcap+'   Price = '+ price+'   Index = '+ index
            print(string)
            config.set(section, "datetime", datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            config.set(section, "price", price)
            config.set(section, "marketcap", marketcap)
            config.set(section, "index", index)
            with open(path, "w") as config_file:
                config.write(config_file)
            driver.quit()
        except Exception as e:
            print ("Something wrong, killing chrome")
            print ("Error: {}".format(e))
            tracebackError = traceback.format_exc()
            print (tracebackError)
            driver.quit()

    print ("Sleeping 60")
    time.sleep(60)








