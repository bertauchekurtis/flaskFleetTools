from flask import Flask, render_template, session, request, redirect, url_for
import fleetData as fd
from datetime import datetime

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
    return render_template("circulation.j2",
                           startDateLabel = leftColumnData[0],
                           endDateLabel = leftColumnData[1],
                           game = leftColumnData[2])

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