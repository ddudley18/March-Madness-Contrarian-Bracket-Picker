# pip install bs4
# pip install requests
# pip install selenium
# pip install webdriver_manager

import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

#Default window size used when setting visiblity of Chrome
WINDOW_SIZE = "1920,1080"


#Get URLs of both websites
predictedChancesURL = "https://www.sportingnews.com/us/ncaa-basketball/news/march-madness-odds-2022-projections/wkmgsmhrbp6xifahweslv1iw"
pickRateURL = "https://fantasy.espn.com/tournament-challenge-bracket/2022/en/whopickedwhom"

#Initiate the webdriver. Path specifies location of the webdriver.
service=Service(ChromeDriverManager().install())

#Make Chrome open window silently (not visible)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

#Get webpage at predictedChancesURL
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(predictedChancesURL)

#Ensures page is loaded
time.sleep(5);

# Stores the information at predictedChancesURL as static HTML
predictedChancesPage = driver.page_source

# Stores the information at pickRateURL as static HTML
pickRatePage = requests.get(pickRateURL)

#Use BeautifulSoup library to grab content of predictedChancesPage
predChancesContent = BeautifulSoup(predictedChancesPage, "html.parser")

#Use BeautifulSoup library to grab content of pickRatePage
pickRateContent = BeautifulSoup(pickRatePage.content, "html.parser")
