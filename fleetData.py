# fleetData.py

import os
from datetime import datetime

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