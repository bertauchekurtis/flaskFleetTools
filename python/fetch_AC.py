from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date
import pandas as pd
import os
import sys
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
args = sys.argv

USERNAME = args[1]
PASSWORD = args[2]

driver.get("https://www.airline-club.com/")

# login to AC
element = driver.find_element(By.ID, "loginUserName")
element.clear()
element.send_keys(USERNAME)
element = driver.find_element(By.ID, "loginPassword")
element.clear()
element.send_keys(PASSWORD)
sleep(1)
element.send_keys(Keys.RETURN)
sleep(5)

# close the announcment pop-up
element = driver.find_element(By.XPATH, "//div[@id='announcementModal']//span[@class='close']")
element.click()
sleep(1)

# navigate to the airplane page
# element = driver.find_element(By.XPATH, "//li[@class='button left-tab user-specific-tab airplaneCanvasTab']/div/div")
# # button is hidden so use js to click
# driver.execute_script("$(arguments[0]).click();", element)
# sleep(5)

# # now we are on the airplane purchase page
# airplaneTabs = driver.find_elements(By.XPATH, "//div[@id='airplaneCanvas']//div[@class='table-row clickable']")
# planeNameAndNumInCirculation = []

# # get all the data
# for elem in airplaneTabs:
#     # elem.click()
#     driver.execute_script("arguments[0].click();", elem)
#     sleep(1)
#     tableRows = driver.find_elements(By.XPATH, "//div[@id='airplaneModelDetail']/div[@class='section']/div[@class='table']/div[@class='table-row']")
#     nameRow = tableRows[0]
#     numRow = tableRows[13]
#     modelName = nameRow.text
#     modelName = modelName.replace("Model:", "")
#     modelName = modelName.replace("\n", "")
#     numInCirculation = numRow.text
#     numInCirculation = numInCirculation.replace("Total in Circulation:", "")
#     numInCirculation = int(numInCirculation)
#     print(modelName)
#         #print(numInCirculation)
#     planeNameAndNumInCirculation.append([modelName, numInCirculation])

 
# # write to file
# sleep(1)
# df = pd.DataFrame(planeNameAndNumInCirculation, columns=['Model', 'NumberInCirculation'])
cwd = os.getcwd()
today = date.today()
stringData = today.strftime("%b-%d-%Y")
# #path = cwd + "/" + stringData + "planeReport.csv"
# #df.to_csv(path_or_buf = path, index = False, escapechar = ' ')

# #df = pd.read_csv("Dec-29-2022planeReport")
# # now we get the fleets
# # navigate to the airplane page
# sleep(10)
# element = driver.find_element(By.XPATH, "//li[@class='button left-tab user-specific-tab rivalsCanvasTab']/div/div")
# # button is hidden so use js to click
# sleep(10)
# driver.execute_script("$(arguments[0]).click();", element)
# sleep(10)

# # grab all the clickable airlines
# airlineTabs = driver.find_elements(By.XPATH, "//div[@id='rivalsTable']//div[@class='table-row clickable']")
# sleep(10)
# # setup df
# listOfPlaneTypes = df['Model'].tolist()
# listOfPlaneTypes.insert(0, "Total")
# listOfPlaneTypes.insert(0, "Airline")
# fleetdf = pd.DataFrame(columns = listOfPlaneTypes)

# for elem in airlineTabs:
#     # elem.click()
#     driver.execute_script("arguments[0].click();", elem)
#     sleep(2)
#     airlineName = driver.find_element(By.XPATH, "//div[@id='rivalDetails']//span[@class='airlineName']")
#     airlineName = airlineName.text
#     print(airlineName)
#     thisAirlineList = []
#     thisAirlineList.append(["Airline", airlineName])
#     totalSize = 0

#     # get fleet elements
#     fleetElements = driver.find_elements(By.XPATH, "//div[@id='rivalDetails']//div[@class='table data fleetList']/div[@class='table-row']/div[@class='cell']")
#     for i in range(0, len(fleetElements), 2):
#         #print(fleetElements[i].text)
#         #print(fleetElements[i+1].text)
#         totalSize += int(fleetElements[i+1].text)
#         thisAirlineList.append([fleetElements[i].text, int(fleetElements[i+1].text)])

#     thisAirlineList.insert(1, ["Total", totalSize])

#     # now make into df and append to master frame
#     thisAirlineDF = pd.DataFrame(thisAirlineList)
#     thisAirlineDF = thisAirlineDF.transpose()
#     toBeNamed = thisAirlineDF.iloc[0]
#     thisAirlineDF.drop([0], inplace = True)
#     thisAirlineDF.rename(columns = toBeNamed, inplace = True)
#     fleetdf = pd.concat([fleetdf, thisAirlineDF], axis=0, ignore_index=True)




# fleetdf.fillna(0,inplace=True)
# path = "./data/AC/" + stringData + "-AC-fleetReport.csv"
# fleetdf.to_csv(path_or_buf = path, index = False, escapechar = ' ')

sleep(10)
element = driver.find_element(By.XPATH, "//li[@class='button left-tab user-specific-tab allianceCanvasTab']/div/div")
# button is hidden so use js to click
sleep(10)
driver.execute_script("$(arguments[0]).click();", element)
sleep(10)

# grab all the clickable alliances
allianceTabs = driver.find_elements(By.XPATH, "//div[@id='allianceTable']//div[@class='table-row clickable']")
sleep(10)

allianceDf = pd.DataFrame(columns=['alliance','members'])

for elem in allianceTabs:
    # elem.click()
    driver.execute_script("arguments[0].click();", elem)
    sleep(2)
    allianceName = driver.find_element(By.XPATH, "//div[@id='allianceDetails']//span[@class='allianceName']")
    allianceName = allianceName.text
    print(allianceName)




    thisAllianceList = []


    # get fleet elements
    allianceMembers = driver.find_elements(By.XPATH, "//div[@id='allianceDetails']//div[@id='allianceMemberList']/div[@class='table-row clickable']/div[@class='cell']")
    for i in range(0, len(allianceMembers), 4):
        print(allianceMembers[i:i+3])
        #print(fleetElements[i].text)
        #print(fleetElements[i+1].text)
        thisAllianceList.append(allianceMembers[i+1].text)
    
    allianceDf = allianceDf.append({"alliance":allianceName,"members":','.join(thisAllianceList)})

path = "./data/AC/" + stringData + "-AC-fleetReport_alliances.csv"
allianceDf.to_csv(path_or_buf = path, index = False, escapechar = ' ')

driver.quit()
