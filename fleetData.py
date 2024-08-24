# fleetData.py

import os
from datetime import datetime
import pandas as pd

def getDateTupleList(game = None):
    if game is not None:
        fileNames = os.listdir("./data/" + game)
        tupleList = []
        for fileName in fileNames:
            month = fileName[:3]
            day = fileName[4:6]
            year = fileName[7:11]
            thisDateTime = datetime.strptime(fileName[:11], "%b-%d-%Y")
            tupleList.append((month, day, year, thisDateTime))
        return sorted(tupleList, key = lambda x: x[3], reverse = True)
    return False

def convertStringToDateTime(string):
    thisDateTime = datetime.strptime(string, "%b%d%Y")
    return thisDateTime

def convertFileNameToDateTime(string):
    thisDateTime = datetime.strptime(string[:11], "%b-%d-%Y")
    return thisDateTime

def convertDateTimeToLabel(date: datetime):
    return date.strftime("%b %d, %Y")

def getFileName(date: datetime, game):
    fileName = date.strftime("%b-%d-%Y-") + game + "-fleetReport.csv"
    return fileName

def getAllFiles(game):
    files = os.listdir("./data/" + game)
    return files

def getCirculationDfs(startDate: datetime, endDate: datetime, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    oldCondensed = createCondensedDF(oldData)
    newCondensed = createCondensedDF(newData)

    mostPopularAircraftDf = createMostPopularAircraftDf(oldCondensed, newCondensed)
    biggestChangesAircraftDf = createBiggestChangesAircraftDf(mostPopularAircraftDf)
    fastestGrowingAircraftDf = createFastestGrowingPopularityAircraftDf(mostPopularAircraftDf)
    fastestShrinkingAircraftdf = createFastestShrinkingPopularityAircraftDf(mostPopularAircraftDf)
    return(mostPopularAircraftDf, biggestChangesAircraftDf, fastestGrowingAircraftDf, fastestShrinkingAircraftdf)

def createCondensedDF(frame: pd.DataFrame):
    df = frame.copy()
    df = df.drop(["Airline", "Total"], axis = 1)
    df = df[sorted(df.columns)]
    condensed = pd.DataFrame(columns = ['Aircraft', 'Total'])
    for column in df.columns:
        condensed = pd.concat([condensed,pd.DataFrame.from_dict({'Aircraft': [column],
                                      'Total': [df[column].sum()]})], ignore_index = True)
    return condensed

def createRawCirculationChangesDF(oldCondensed: pd.DataFrame, newCondensed: pd.DataFrame):
    rawDf = newCondensed.copy()
    rawDf["Old Total"] = oldCondensed["Total"]
    rawDf["Change"] = pd.to_numeric(rawDf["Total"]) - pd.to_numeric(rawDf["Old Total"])
    rawDf.columns = ["Aircraft", "New Total", "Old Total", "Change"]
    return rawDf.loc[:,["Aircraft", "Old Total", "New Total", "Change"]]

def createMostPopularAircraftDf(oldCondensed: pd.DataFrame, newCondensed: pd.DataFrame):
    old = oldCondensed.copy()
    new = newCondensed.copy()
    old.columns = ["Aircraft", "Old Total"]
    new.columns = ["Aircraft", "New Total"]
    df = pd.merge(old, new, on = "Aircraft")
    df["Change"] = pd.to_numeric(df["New Total"]) - pd.to_numeric(df["Old Total"])
    df = df.sort_values(by = "New Total", ascending = False)
    df["Rank"] = df["New Total"].rank(ascending = False, method = "max")
    df["Rank"] = df["Rank"].astype(int)
    df = df[["Rank", "Aircraft", "Old Total", "New Total", "Change"]]
    return df

def createBiggestChangesAircraftDf(mostPopularDf: pd.DataFrame):
    df = mostPopularDf.copy()
    df["abs"] = abs(df["Change"])
    df = df.sort_values(by = "abs", ascending = False)
    df = df.drop("abs", axis = 1)
    df["Rank"] = df["Change"].abs().rank(ascending = False, method = "max")
    df["Rank"] = df["Rank"].astype(int)
    return df

def createFastestGrowingPopularityAircraftDf(mostPopularDf: pd.DataFrame):
    df = mostPopularDf.copy()
    df = df.sort_values(by = "Change", ascending = False)
    df["Rank"] = df["Change"].rank(ascending = False, method = "max")
    df["Rank"] = df["Rank"].astype(int)
    return df

def createFastestShrinkingPopularityAircraftDf(mostPopularDf: pd.DataFrame):
    df = mostPopularDf.copy()
    df = df.sort_values(by = "Change", ascending = True)
    df["Rank"] = df["Change"].rank(ascending = True, method = "max")
    df["Rank"] = df["Rank"].astype(int)
    return df

def getFleetDfs(startDate: datetime, endDate: datetime, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)
    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)
    largestFleetsDf = createLargestFleetsDf(oldData, newData)
    fastestGrowingFleetsDf = createLargestGrowingFleetsDf(largestFleetsDf)
    fastestShrinkingFleetsDf = createLargestShrinkingFleetsDf(largestFleetsDf)
    return (largestFleetsDf, fastestGrowingFleetsDf, fastestShrinkingFleetsDf)

def createLargestFleetsDf(oldData: pd.DataFrame, newData: pd.DataFrame):
    old_largest = pd.DataFrame({'Airline': oldData['Airline'], 'Old Total': oldData['Total']})
    new_largest = pd.DataFrame({'Airline': newData['Airline'], 'New Total': newData['Total']})
    combined = pd.merge(old_largest, new_largest, on = 'Airline', how = 'outer')
    combined = combined.fillna(0)
    combined['New Total'] = combined["New Total"].astype(int)
    combined['Old Total'] = combined["Old Total"].astype(int)
    combined["Change"] = combined["New Total"] - combined["Old Total"]
    combined = combined.sort_values(by = "New Total", ascending = False)
    combined["Rank"] = combined["New Total"].rank(ascending = False, method = "max").astype(int)
    return combined.loc[:,["Rank", "Airline", "Old Total", "New Total", "Change"]]

def createLargestGrowingFleetsDf(largestFleetsDf: pd.DataFrame):
    df = largestFleetsDf.copy()
    df = df.sort_values(by = "Change", ascending = False)
    df["Rank"] = df["Change"].rank(ascending = False, method = "max").astype(int)
    return df

def createLargestShrinkingFleetsDf(largestFleetsDf: pd.DataFrame):
    df = largestFleetsDf.copy()
    df = df.sort_values(by = "Change", ascending = True)
    df["Rank"] = df["Change"].rank(ascending = True, method = "max").astype(int)
    return df

def getAllAirlines(startDate: datetime, endDate: datetime, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    allAirlines = oldData['Airline'].tolist() + newData['Airline'].tolist()
    return list(set(allAirlines))

def getAirlineTable(startDate: datetime, endDate: datetime, airline, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    oldData = oldData.loc[oldData['Airline'] == airline]
    newData = newData.loc[newData['Airline'] == airline]
    
    oldData = oldData.reindex(sorted(oldData.columns), axis = 1)
    newData = newData.reindex(sorted(newData.columns), axis = 1)

    if oldData.empty:
        oldData.loc[0] = [0] * len(oldData.columns)
    if newData.empty:
        newData.loc[0] = [0] * len(newData.columns)

    oldData = oldData.drop('Airline', axis = 1)
    newData = newData.drop('Airline', axis = 1)
    oldData = oldData.reset_index(drop = True)
    newData = newData.reset_index(drop = True)
    diff = newData.astype(int) - oldData.astype(int)
    
    allData = pd.concat([oldData, newData, diff])
    allData = allData.loc[:, (allData != 0).any(axis = 0)]
    allData[airline] = ["Old", "New", "Change"]
    allData.set_index(airline, inplace = True)
    allData = allData.transpose()

    if allData.empty:
        allData.loc[0] = [0] * len(allData.columns)

    return allData

def getAirlineHistory(airline, game):
    allGameFiles = getAllFiles(game)
    airlineHistoryEntires = []
    airlineDetailEntries = []
    for gameFile in allGameFiles:
        df = pd.read_csv("./data/" + game + "/" + gameFile)
        try:
            thisTotal = df.loc[df['Airline'] == airline, 'Total'].values[0]
            row = df.loc[df['Airline'] == airline].iloc[0]
            row['date'] = convertFileNameToDateTime(gameFile)
            airlineDetailEntries.append(row.to_dict())
            airlineHistoryEntires.append((thisTotal, convertFileNameToDateTime(gameFile)))
        except:
            airlineHistoryEntires.append((0, convertFileNameToDateTime(gameFile)))
            airlineDetailEntries.append({'date': convertFileNameToDateTime(gameFile)})
    detailed_df = pd.DataFrame(airlineDetailEntries)
    detailed_df = detailed_df.fillna(0)
    non_zero = detailed_df.columns[(detailed_df != 0).any()]
    detailed_df = detailed_df[non_zero]
    detailed_df = detailed_df.sort_values(by = 'date')
    print(detailed_df)
    return sorted(airlineHistoryEntires, key = lambda x: x[1]), 0
        

def getAllAircrafts(startDate: datetime, endDate: datetime, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    oldData = oldData.drop('Airline', axis = 1)
    newData = newData.drop('Airline', axis = 1)

    oldData = oldData.drop('Total', axis = 1)
    newData = newData.drop('Total', axis = 1)

    allAircrafts = oldData.columns.tolist() + newData.columns.tolist()
    return sorted(list(set(allAircrafts)))

def getAircraftTable(startDate: datetime, endDate: datetime, aircraft, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    oldData = oldData[["Airline", aircraft]]
    newData = newData[["Airline", aircraft]]

    oldData = oldData.rename(columns = {aircraft: "Old Total"})
    newData = newData.rename(columns = {aircraft: "New Total"})

    combined = pd.merge(oldData, newData, on = "Airline", how = 'outer')
    combined = combined.fillna(0)
    combined = combined.loc[~((combined['Old Total'] == 0.0) & (combined['New Total'] == 0.0))]
    combined['Old Total'] = combined['Old Total'].astype(int)
    combined['New Total'] = combined['New Total'].astype(int)
    combined['Change'] = combined['New Total'] - combined['Old Total']
    combined = combined.sort_values('New Total', ascending = False)
    combined = pd.concat([combined, pd.DataFrame.from_dict({'Airline' : ['Total'],
                            'Old Total' : [combined['Old Total'].sum()],
                            'New Total' : [combined['New Total'].sum()],
                            'Change' : [combined['Change'].sum()]})], 
                            ignore_index = True)
    # combined = combined.append({'Airline' : 'Total',
    #                         'Old Total' : combined['Old Total'].sum(),
    #                         'New Total' : combined['New Total'].sum(),
    #                         'Change' : combined['Change'].sum()},
    #                         ignore_index = True)
    return(combined)