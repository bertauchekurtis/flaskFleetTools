from flask import Flask, render_template, session, request, jsonify
import fleetData as fd

app = Flask(__name__)
app.secret_key = 'very_secret_key'

@app.route("/")
def index():
    leftColumnData = getLeftColumnInfo()
    return render_template("home.j2", 
                            game = leftColumnData[2], 
                            dates = leftColumnData[3], 
                            startDateLabel = leftColumnData[0],
                            endDateLabel = leftColumnData[1])

@app.route("/set_game", methods = ['POST'])
def setGame():
    varName = request.args.get("var", None)
    val = request.args.get("val", None)
    if(varName is not None and val is not None):
        print(varName, val)
        session[varName] = val
        if(varName == "game"):
            print("HERE")
            try:
                session.pop("start")
                session.pop("end")
            except:
                pass
        return {"result" : "success"}
    return {"result" : "failure"}

@app.route("/set_date", methods = ['POST'])
def setDate():
    dateString = request.args.get("date", None)
    type = request.args.get("type", None)

    if(dateString is not None and type in ("start", "end")):
        print(dateString, type)
        newDate = fd.convertStringToDateTime(dateString)
        session[type] = newDate
        return {"result" : "success"}
    return {"result" : "failure"}

@app.route("/circulation_changes")
def circulationChanges():
    leftColumnData = getLeftColumnInfo()
    mostPopularAircraftDf = None
    biggestChangesAircraftDf = None
    fastestShrinkingAircraftdf = None
    fastestGrowingAircraftDf = None

    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        mostPopularAircraftDf, biggestChangesAircraftDf, fastestGrowingAircraftDf, fastestShrinkingAircraftdf = fd.getCirculationDfs(session['start'], session['end'], session['game'])

    return render_template("circulation.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           mostPopularAircraftDf = mostPopularAircraftDf,
                           biggestChangesAircraftDf = biggestChangesAircraftDf,
                           fastestGrowingAircraftDf =fastestGrowingAircraftDf,
                           fastestShrinkingAircraftdf = fastestShrinkingAircraftdf,
                           top20df = mostPopularAircraftDf)

def getLeftColumnInfo():
    # initialize them to none
    startLabel = None
    endLabel = None
    game = None
    availableDates = None

    # fill with info from session
    if 'game' in session:
        game = session['game']
        availableDates = fd.getDateTupleList(game)

    if 'start' in session:
        startLabel = fd.convertDateTimeToLabel(session['start'])
    if 'end' in session:
        endLabel = fd.convertDateTimeToLabel(session['end'])
    
    return(startLabel, endLabel, game, availableDates)

@app.route("/fleet_changes")
def fleetChanges():
    leftColumnData = getLeftColumnInfo()

    largestFleetsDf = None
    fastestGrowingFleetsDf = None
    fastestShrinkingFleetsDf = None

    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        largestFleetsDf, fastestGrowingFleetsDf, fastestShrinkingFleetsDf = fd.getFleetDfs(session['start'], session['end'], session['game'])

    return render_template("fleets.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           largestFleetsDf = largestFleetsDf,
                           fastestGrowingFleetsDf = fastestGrowingFleetsDf,
                           fastestShrinkingFleetsDf = fastestShrinkingFleetsDf)


@app.route("/clear_cookies", methods = ['POST'])
def clearCookie():
    session.clear()
    return {"result": "success"}

@app.route("/discord_message")
def discordMessage():
    leftColumnData = getLeftColumnInfo()

    mostPopularAircraftDf = None
    biggestChangesAircraftDf = None
    largestFleetsDf = None
    fastestGrowingFleetsDf = None
    fastestShrinkingFleetsDf = None

    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        mostPopularAircraftDf, biggestChangesAircraftDf, _, _ = fd.getCirculationDfs(session['start'], session['end'], session['game'])
        largestFleetsDf, fastestGrowingFleetsDf, fastestShrinkingFleetsDf = fd.getFleetDfs(session['start'], session['end'], session['game'])
        largestFleetsDf['Old Rank'] = largestFleetsDf["Old Total"].rank(ascending = False, method = "max")
        fastestShrinkingFleetsDf['Change'] = abs(fastestShrinkingFleetsDf["Change"].astype(int))
    return render_template("discord.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           mostPopularAircraftDf = mostPopularAircraftDf,
                           biggestChangesAircraftDf = biggestChangesAircraftDf,
                           largestFleetsDf = largestFleetsDf,
                           fastestGrowingFleetsDf = fastestGrowingFleetsDf,
                           fastestShrinkingFleetsDf = fastestShrinkingFleetsDf)

@app.route("/airline_search")
def airlineSearch():
    leftColumnData = getLeftColumnInfo()

    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    airlineDict = {}
    for letter in letters:
        airlineDict[letter] = []

    
    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        allAirlines = fd.getAllAirlines(session['start'], session['end'], session['game'])
        allAirlines = sorted(allAirlines)
        for airline in allAirlines:
            letter = airline.upper()[0]
            airlineDict[letter].append(airline)

    return render_template("chooseAirline.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           letters = letters,
                           airlineDict = airlineDict)

@app.route("/showAirline")
def showAirline():
    leftColumnData = getLeftColumnInfo()

    airline = request.args.get("airline", None)
    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        airlineTable = fd.getAirlineTable(session['start'], session['end'], airline, session['game'])
        history = fd.getAirlineHistory(airline, session['game'])
    return render_template("showAirline.j2",
                    startDateLabel = leftColumnData[0],
                    endDateLabel = leftColumnData[1],
                    game = leftColumnData[2],
                    airlinetable = airlineTable,
                    airline = airline)

@app.route("/getAirlineHistory")
def returnAirlineHistory():
    leftColumnData = getLeftColumnInfo()
    totals = []
    dates = []
    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        airline = request.args.get("airline", None)
        history, details = fd.getAirlineHistory(airline, session['game'])
        for t in history:
            totals.append(int(t[0]))
            dates.append(fd.convertDateTimeToLabel(t[1]))
    return(jsonify(totals = totals, dates = dates))

@app.route("/aircraftSearch")
def aircraftSearch():
    leftColumnData = getLeftColumnInfo()
    manuDict = {}
    aircrafts = fd.getAllAircrafts(session['start'], session['end'], session['game'])
    for plane in aircrafts:
        manu = plane.split(" ")[0]
        if manu in manuDict.keys():
            manuDict[manu].append(plane)
        else:
            manuDict[manu] = [plane]
    
    return render_template("chooseAircraft.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           manuDict = manuDict)

@app.route("/showAircraft")
def showAircraft():
    leftColumnData = getLeftColumnInfo()
    aircraft = request.args.get("aircraft", None)
    if(leftColumnData[0] is not None and leftColumnData[1] is not None and leftColumnData[2] is not None):
        aircraftTable = fd.getAircraftTable(session['start'], session['end'], aircraft, session['game'])
    return render_template("showAircraft.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2],
                           aircraftTable = aircraftTable,
                           aircraft = aircraft)