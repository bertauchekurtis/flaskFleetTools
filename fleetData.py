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

def convertDateTimeToLabel(date: datetime):
    return date.strftime("%b %d, %Y")

def getFileName(date: datetime, game):
    fileName = date.strftime("%b-%d-%Y-") + game + "-fleetReport.csv"
    return fileName

def getCirculationDfs(startDate: datetime, endDate: datetime, game):
    oldFileName = getFileName(startDate, game)
    newFileName = getFileName(endDate, game)

    oldData = pd.read_csv("./data/" + game + "/" + oldFileName)
    newData = pd.read_csv("./data/" + game + "/" + newFileName)

    oldCondensed = createCondensedDF(oldData)
    newCondensed = createCondensedDF(newData)

    rawCirculationDf = createRawCirculationChangesDF(oldCondensed, newCondensed)
    mostPopularAircraftDf = createMostPopularAircraftDf(oldCondensed, newCondensed)
    print(mostPopularAircraftDf)
    biggestChangesAircraftDf = createBiggestChangesAircraftDf(mostPopularAircraftDf)
    print(biggestChangesAircraftDf.head(20))
    fastestGrowingAircraftDf = createFastestGrowingPopularityAircraftDf(mostPopularAircraftDf)
    print(fastestGrowingAircraftDf)
    fastestShrinkingAircraftdf = createFastestShrinkingPopularityAircraftDf(mostPopularAircraftDf)
    print(fastestShrinkingAircraftdf)
    return(mostPopularAircraftDf, biggestChangesAircraftDf, fastestGrowingAircraftDf, fastestShrinkingAircraftdf)




def createCondensedDF(frame: pd.DataFrame):
    df = frame.copy()
    df = df.drop(["Airline", "Total"], axis = 1)
    df = df[sorted(df.columns)]
    condensed = pd.DataFrame(columns = ['Aircraft', 'Total'])
    for column in df.columns:
        condensed = condensed.append({'Aircraft': column,
                                      'Total': df[column].sum()},
                                      ignore_index = True)
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