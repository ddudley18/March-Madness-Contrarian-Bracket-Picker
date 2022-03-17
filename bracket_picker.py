
# Notes: Make sure python interpreter is set to virtualenv python file

# from difflib import diff_bytes
import requests, time, operator
import array as arr

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Enter a number x, [1, 64], to display top x best value picks for each round.
NUMBER_OF_RANKINGS = 5

# Default window size used when setting visiblity of Chrome.
WINDOW_SIZE = "1920,1080"

# Get URLs of both websites.
predictedChancesURL = "https://www.sportingnews.com/us/ncaa-basketball/news/march-madness-odds-2022-projections/wkmgsmhrbp6xifahweslv1iw"
pickRateURL = "https://fantasy.espn.com/tournament-challenge-bracket/2022/en/whopickedwhom"

# Initiate the webdriver. Path specifies location of the webdriver.
service=Service(ChromeDriverManager().install())

# Make Chrome open window silently (not visible).
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

# Get webpage at predictedChancesURL.
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(predictedChancesURL)

# Ensures page is loaded.
time.sleep(5);

# Stores the information at predictedChancesURL as static HTML.
predictedChancesPage = driver.page_source

# Stores the information at pickRateURL as static HTML.
pickRatePage = requests.get(pickRateURL)

# Use BeautifulSoup library to grab content of predictedChancesPage.
predChancesContent = BeautifulSoup(predictedChancesPage, "html.parser")

# Use BeautifulSoup library to grab content of pickRatePage.
pickRateContent = BeautifulSoup(pickRatePage.content, "html.parser")


# Gets rows of predicted chances table for each region and create list of regions.
regions = [];
eastRegionPred = predChancesContent.find_all("table")[4].find("tbody").find_all("tr")
midwestRegionPred = predChancesContent.find_all("table")[6].find("tbody").find_all("tr")
southRegionPred = predChancesContent.find_all("table")[8].find("tbody").find_all("tr")
westRegionPred = predChancesContent.find_all("table")[10].find("tbody").find_all("tr")
regions.extend([eastRegionPred, midwestRegionPred, southRegionPred, westRegionPred])

# Get rows of table with pick rates.
pickRateData = pickRateContent.find("table").find("tbody").find_all("tr")

#Initialize dictionary with nested dictionary for each tRound to store predicted chances.
predChancesDict = { 'r1': { },
                    'r2': { },
                    'r3': { },
                    'r4': { },
                    'r5': { },
                    'r6': { }}
                    
#Initialize dictionary with nested dictionary for each tRound to store pick rates.
pickRateDict = { 'r1': { },
                 'r2': { },
                 'r3': { },
                 'r4': { },
                 'r5': { },
                 'r6': { }}

#Initialize dictionary with nested dictionary for each tRound to store results (differentials).
differentialsDict = { 'r1': { },
                      'r2': { },
                      'r3': { },
                      'r4': { },
                      'r5': { },
                      'r6': { }}

# Add to nested dictionaries describing predicted chances for each tournament round (tRound).
pastSeed = 0
for region in regions:
    for row in region:
        curSeed = int(row.select("tr > td")[0].get_text(strip="true"))
        if (curSeed != pastSeed):
            name = row.select("tr > td")[1].get_text(strip="true")
            for tRound in range(1,7):
                teamPredChance = row.select("tr > td")[tRound + 1].get_text(strip="true")
                tRound = 'r' + str(tRound)
                predChancesDict[tRound][name] = float(teamPredChance.strip("%"))
            pastSeed = curSeed

# Add to nested dictionaries describing pick rate for each tournament round (tRound).
for row in pickRateData:
    for tRound in range(1,7):
        entry = row.select("tr > td")[tRound - 1].find_all("span")
        name = entry[1].get_text(strip="true")
        teamPickRate = entry[3].get_text(strip="true")
        tRound = 'r' + str(tRound)
        pickRateDict[tRound][name] = float(teamPickRate.strip("%"))
        
# Function for converting between differences in naming between both websites.
def getAltName(team):
    if team == "South Dakota State":
        return "S Dakota St"
    elif team == "Jacksonville State":
        return "J'Ville St"
    elif team == "Rutgers":
        return "Notre Dame"
    elif team =="New Mexico State":
        return "New Mexico St"
    elif team =="CS Fullerton":
        return "CSU Fullerton"
    else:
        return None

# Counter used to specify round for each data output.
curRound = 1

# Header for command line output.
print("\n********************************\n********************************")
print("Best March Madness Contrarian Picks For Each Round")
print("\n********************************\n********************************")
print("""Note: Best value picks are displayed ordered form top to bottom for winning the respective round.
        More negative differentials indicate better value, while positive differentials indicate worse value.\n""")

# Find differential between a team's pick rate and their simulated chances to advance.
for tRound in predChancesDict:
    for team, chances in predChancesDict[tRound].items():
        pickRate = pickRateDict[tRound].get(team)
        try:
            differential = round(pickRate - chances, 2)
        except:
            team = getAltName(team)
            pickRate = pickRateDict[tRound].get(team)
            differential = round(pickRate - chances, 2)
        differentialsDict[tRound][team] = differential
    differentialsDict[tRound] = dict(sorted(differentialsDict[tRound].items(), key=lambda item: item[1]))

    # Print amount of picks specified by NUMBER_OF_RANKINGS with the best value
    n = 0
    keys = differentialsDict[tRound].keys()
    print("ROUND: " + str(curRound))
    while n < NUMBER_OF_RANKINGS:
        print(list(keys)[n] + ": " + str(differentialsDict[tRound].get(list(keys)[n])))
        n+=1
    print("\n")
    curRound+=1













        




