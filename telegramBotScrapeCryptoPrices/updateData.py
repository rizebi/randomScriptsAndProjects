import traceback # for error handling
import configparser
import undetected_chromedriver.v2 as uc
import time
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver # for scraping
from selenium.webdriver.chrome.options import Options

path = "settings.ini"


while 1<2:

    config = configparser.ConfigParser()
    config.read(path)


    for section in config.sections():
        address = config.get(section, "address")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36")
        driver = webdriver.Chrome(chrome_options=chrome_options)

        try:     
            print ('https://charts.bogged.finance/?token=' + address)
            driver.get('https://charts.bogged.finance/?token=' + address)  # known url using cloudflare's "under attack mode"
            print ("Sleeping 5 sec for security check")
            time.sleep (5)
            #driver.save_screenshot('poocoin.png')
            content = driver.page_source
            #print ("CONTENT:")
            #print (content)
            #print ("End content")
            soup = BeautifulSoup(content, features="html.parser")
            divMarketCap = soup.findAll('div', attrs={'class':'my-1 flex flex-row justify-start space-x-3 md:pt-0 pt-3 sm:space-x-6 w-full md:w-auto border-t md:border-t-0 border-gray-200 dark:border-gray-700'})
            for span in divMarketCap[0].findAll('span'):
                if "Marketcap" in str(span) and "$" in str(span):
                    marketcap = span.findAll('h4')[0].text.strip()

            price = "$" + str(soup.findAll('title')).split("$")[1].split(" ")[0]
            
            print(datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            string = 'Market Cap= '+marketcap+'   Price = '+ price
            print(string)
            config.set(section, "datetime", datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)"))
            config.set(section, "price", price)
            config.set(section, "marketcap", marketcap)
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








