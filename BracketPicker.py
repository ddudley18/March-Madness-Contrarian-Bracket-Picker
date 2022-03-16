
# Notes: Make sure python interpreter is set to virtualenv python file

import requests, time
import array as arr

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


#Gets rows of predicted chances table for each region
regions = [];
eastRegionPred = predChancesContent.find_all("table")[4].find("tbody").find_all("tr")
midwestRegionPred = predChancesContent.find_all("table")[6].find("tbody").find_all("tr")
southRegionPred = predChancesContent.find_all("table")[8].find("tbody").find_all("tr")
westRegionPred = predChancesContent.find_all("table")[10].find("tbody").find_all("tr")
regions.extend([eastRegionPred, midwestRegionPred, southRegionPred, westRegionPred])

# Get rows of table with pick rates
pickRateData = pickRateContent.find("table").find("tbody").find_all("tr")

#Initialize dictionary with nested dictionary for each round to store predicted chances
predChancesDict = { 'r1': { },
                    'r2': { },
                    'r3': { },
                    'r4': { },
                    'r5': { },
                    'r6': { }}
                    
#Initialize dictionary with nested dictionary for each round to store pick rates
pickRateDict = { 'r1': { },
                 'r2': { },
                 'r3': { },
                 'r4': { },
                 'r5': { },
                 'r6': { }}

# Add to nested dictionaries describing predicted chances for each round
for region in regions:
    for row in region:
        name = row.select("tr > td")[1].get_text(strip="true")
        for round in range(1,7):
            teamPredChance = row.select("tr > td")[round + 1].get_text(strip="true")
            round = 'r' + str(round)
            predChancesDict[round][name] = float(teamPredChance.strip("%"))

# Add to nested dictionaries describing pick rate for each round
for row in pickRateData:
    for round in range(1,7):
        entry = row.select("tr > td")[round - 1].find_all("span")
        name = entry[1].get_text(strip="true")
        teamPickRate = entry[3].get_text(strip="true")
        round = 'r' + str(round)
        pickRateDict[round][name] = float(teamPickRate.strip("%"))












        




