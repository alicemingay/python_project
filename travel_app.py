from flask import Flask, render_template, request
import requests

app = Flask("app")

with open("credentials.txt","r") as file:
    R2R_API = file.readline().split()[2]
    MAILGUN_API = file.readline().split()[2]
    MAILGUN_DOMAIN_NAME = file.readline().split()[2]
    ZOMATO_API = file.readline().split()[2]

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
    "start_point" : r["places"][0]["longName"],
    "end_point" : r["places"][1]["longName"],
    "route_0_name" : r["routes"][0]["name"],
    "route_0_arrPlace" : r["routes"][0]["arrPlace"],
    "route_0_depPlace" : r["routes"][0]["depPlace"],
    "route_0_distance" : r["routes"][0]["distance"],
    "route_0_totalDuration" : r["routes"][0]["totalDuration"],
    "route_0_url" : r["routes"][0]["segments"][0]["agencies"][0]["links"][0]["url"],
    "route_0_currency" : r["routes"][0]["indicativePrices"][0]["nativeCurrency"],
    "route_0_PriceHigh" : r["routes"][0]["indicativePrices"][0]["nativePriceHigh"],
    "route_0_PriceLow" : r["routes"][0]["indicativePrices"][0]["nativePriceLow"],
    "route_0_full" : r["routes"][0],
    }

    latitude = r["places"][1]["lat"]
    longitude = r["places"][1]["lng"]
    place = "Dishoom"
    restaurant = restaurants(place)

    return render_template("results.html", R2R_categories=R2R_categories, restaurant=restaurant)

def restaurants(destination):
    restaurant = destination

    return restaurant


@app.route("/email", methods=["POST"])
def email_address():
    email_recipient = request.form["email"]
    email_content = "hello" #This needs to be set to the right content
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


@app.route("/contact")
def contact():
    return render_template("contact.html")

app.run(debug=True)
