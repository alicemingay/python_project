from flask import Flask, render_template, request
import requests

app = Flask("app")

with open("credentials.txt","r") as file:
    R2R_API = file.readline().split()[2]
    MAILGUN_API = file.readline().split()[2]
    MAILGUN_DOMAIN_NAME = file.readline().split()[2]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/journey", methods=["POST"])
def journey():
    startLocation = request.form["startLocation"]
    destination = request.form["destination"]
    response = getRoute(startLocation, destination)
    return response

@app.route("/results", methods=["GET"])
def getRoute(startLocation, destination):
    endpoint = "http://free.rome2rio.com/api/1.4/json/Search"
    payload = {"key": R2R_API, "oName": startLocation, "dName": destination}
    r = requests.get(endpoint, params=payload).json()

    R2R_categories = {
    "place" : r["places"][9]["shortName"],
    }

    return render_template("results.html", R2R_categories=R2R_categories)

#@app.route("/email", methods=["POST"])
#def send_email():
#        weblink = "https://api.mailgun.net/v3/" + MAILGUN_DOMAIN_NAME + "/messages"
#        auth=("api", MAILGUN_API)
#        data = {"from": "Excited User <mailgun@"+ MAILGUN_DOMAIN_NAME +">",
#               "to": ["alice.mingay@gmail.com"],
#               "subject": "Hello",
#               "text": "Testing some Mailgun awesomness!"}
#        response = requests.post(weblink, auth, data)
#        message = "Your email was successfully sent to the address"
#        return render_template("results.html", message=message)

app.run(debug=True)
