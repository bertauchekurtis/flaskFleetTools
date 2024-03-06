from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = 'very_secret_key'

@app.route("/")
def index():
    if 'game' in session:
        return render_template("index.j2", game = session['game'])
    else:
        return render_template("index.j2")

@app.route("/set_session_variable", methods = ['POST'])
def setSessionVariable():
    varName = request.args.get("var", None)
    val = request.args.get("val", None)
    if(varName is not None and val is not None):
        print(varName, val)
        session[varName] = val
        return {"result" : "success"}
    return {"result" : "failure"}