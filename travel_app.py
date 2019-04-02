from flask import Flask, render_template, request
import requests
import os

app = Flask("app")
port = int(os.environ.get("PORT", 5000))

R2R_API = os.environ.get("R2R_API", None)
MAILGUN_API = os.environ.get("MAILGUN_API", None)
MAILGUN_DOMAIN_NAME = os.environ.get("MAILGUN_DOMAIN_NAME", None)
ZOMATO_API = os.environ.get("ZOMATO_API", None)

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
    payload = {"key": R2R_API, "oName": startLocation, "dName": destination, "noCar": "True", "noRideshare": "True"}
    r = requests.get(endpoint, params=payload).json()

    latitude = r["places"][1]["lat"]
    longitude = r["places"][1]["lng"]
    zomatoInput = restaurants(latitude, longitude, r)

    return zomatoInput

def restaurants(latitude, longitude, r):
    endpoint = "https://developers.zomato.com/api/v2.1/geocode?"
    headers = {"Accept": "application/json", "user-key": ZOMATO_API}
    params = {"lat": latitude, "lon": longitude}
    req = requests.get(endpoint, headers=headers, params=params).json()

    zomatoRestaurants = None

    if "nearby_restaurants" in req:
        zomatoRestaurants = req["nearby_restaurants"]

    R2R_names = {
    "start_point" : r["places"][0]["longName"],
    "end_point" : r["places"][1]["longName"],
    }

    R2R_categories = r["routes"]

    return render_template("results.html", R2R_names=R2R_names, R2R_categories=R2R_categories, zomatoRestaurants=zomatoRestaurants)

@app.route("/email", methods=["POST"])
def email_address():
    email_recipient = request.form["email"]
    email_content = ''
    for field_name, field_value in request.form.items():
      if field_name.startswith("result"):
        email_content += '{}'.format(field_value)
    response = email_confirmation(email_recipient, email_content)
    return response

@app.route("/email_confirmation", methods=["GET"])
def email_confirmation(email_recipient, email_content):
    send_email(email_recipient, email_content)
    message = "Your email was successfully sent to {}".format(email_recipient)
    return render_template("email_confirmation.html", message=message)

def send_email(email_recipient, email_content):
    return requests.post(
        "https://api.mailgun.net/v3/" + MAILGUN_DOMAIN_NAME + "/messages",
        auth=("api", MAILGUN_API),
        data={"from": "Destination ? <mailgun@"+ MAILGUN_DOMAIN_NAME +">",
              "to": [email_recipient],
              "subject": "Your Destination ? Search Results",
              "text": email_content})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/further")
def further_info():
    return render_template("further.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

app.run(host='0.0.0.0', port=port, debug=True)
