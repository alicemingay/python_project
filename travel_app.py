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
    response = requests.get(endpoint, params=payload).json()

    print response
#    print data
#    getRoute = data['main']['temp']
    return render_template("results.html")

#@app.route("/email", methods=["POST"])
#def email_results():
#    "#" = requests.post( #what do I call this?
#        "https://api.mailgun.net/v3/" + MAILGUN_DOMAIN_NAME + "/messages",
#        auth=("api", MAILGUN_API),
#        data={"from": "Destination ? <mailgun@"+ MAILGUN_DOMAIN_NAME +">",
#              "to": ["email"], #how do I set this to raw input?
#              "subject": "Destination ? Search Results",
#              "text": "##"}) #same q as above - need to pull information from previous function
#    response = "Email successfully sent to {}".format(text)
#    return render_template("results.html", response=response)

#json/Search?key=&oName=Bern&dName=Zurich&noRideshare

app.run(debug=True)
