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

    latitude = r["places"][1]["lat"]
    longitude = r["places"][1]["lng"]
    zomatoInput = restaurants(latitude, longitude, r)

    return zomatoInput

def restaurants(latitude, longitude, r):
    endpoint = "https://developers.zomato.com/api/v2.1/geocode?"
    headers = {"Accept": "application/json", "user-key": ZOMATO_API}
    params = {"lat": latitude, "lon": longitude}
    req = requests.get(endpoint, headers=headers, params=params).json()

    zomatoRestaurants = {
    "option_0_name" : req["nearby_restaurants"][0]["restaurant"]["name"],
    "option_0_cuisine" : req["nearby_restaurants"][0]["restaurant"]["cuisines"],
    "option_0_address" : req["nearby_restaurants"][0]["restaurant"]["location"]["address"],
    "option_0_more" : req["nearby_restaurants"][0]["restaurant"]["url"],
    "option_1_name" : req["nearby_restaurants"][1]["restaurant"]["name"],
    "option_1_cuisine" : req["nearby_restaurants"][1]["restaurant"]["cuisines"],
    "option_1_address" : req["nearby_restaurants"][1]["restaurant"]["location"]["address"],
    "option_1_more" : req["nearby_restaurants"][1]["restaurant"]["url"],
    "option_2_name" : req["nearby_restaurants"][2]["restaurant"]["name"],
    "option_2_cuisine" : req["nearby_restaurants"][2]["restaurant"]["cuisines"],
    "option_2_address" : req["nearby_restaurants"][2]["restaurant"]["location"]["address"],
    "option_2_more" : req["nearby_restaurants"][2]["restaurant"]["url"],
    "option_3_name" : req["nearby_restaurants"][3]["restaurant"]["name"],
    "option_3_cuisine" : req["nearby_restaurants"][3]["restaurant"]["cuisines"],
    "option_3_address" : req["nearby_restaurants"][3]["restaurant"]["location"]["address"],
    "option_3_more" : req["nearby_restaurants"][3]["restaurant"]["url"],
    "option_4_name" : req["nearby_restaurants"][4]["restaurant"]["name"],
    "option_4_cuisine" : req["nearby_restaurants"][4]["restaurant"]["cuisines"],
    "option_4_address" : req["nearby_restaurants"][4]["restaurant"]["location"]["address"],
    "option_4_more" : req["nearby_restaurants"][4]["restaurant"]["url"],
    "option_5_name" : req["nearby_restaurants"][5]["restaurant"]["name"],
    "option_5_cuisine" : req["nearby_restaurants"][5]["restaurant"]["cuisines"],
    "option_5_address" : req["nearby_restaurants"][5]["restaurant"]["location"]["address"],
    "option_5_more" : req["nearby_restaurants"][5]["restaurant"]["url"],
    "option_6_name" : req["nearby_restaurants"][6]["restaurant"]["name"],
    "option_6_cuisine" : req["nearby_restaurants"][6]["restaurant"]["cuisines"],
    "option_6_address" : req["nearby_restaurants"][6]["restaurant"]["location"]["address"],
    "option_6_more" : req["nearby_restaurants"][6]["restaurant"]["url"],
    "option_7_name" : req["nearby_restaurants"][7]["restaurant"]["name"],
    "option_7_cuisine" : req["nearby_restaurants"][7]["restaurant"]["cuisines"],
    "option_7_address" : req["nearby_restaurants"][7]["restaurant"]["location"]["address"],
    "option_7_more" : req["nearby_restaurants"][7]["restaurant"]["url"],
    }

    R2R_categories = {
    "start_point" : r["places"][0]["longName"],
    "end_point" : r["places"][1]["longName"],
    "route_0_name" : r["routes"][0]["name"],
    "route_0_arrPlace" : r["routes"][0]["arrPlace"],
    "route_0_depPlace" : r["routes"][0]["depPlace"],
    "route_0_distance" : r["routes"][0]["distance"],
    "route_0_totalDuration" : r["routes"][0]["totalDuration"],
    "route_0_url" : r["routes"][0]["segments"][0]["agencies"][0]["links"][0]["url"],
#    "route_0_currency" : r["routes"][0]["indicativePrices"][0]["nativeCurrency"],
#    "route_0_PriceHigh" : r["routes"][0]["indicativePrices"][0]["nativePriceHigh"],
#    "route_0_PriceLow" : r["routes"][0]["indicativePrices"][0]["nativePriceLow"],
    "route_1_name" : r["routes"][1]["name"],
    "route_1_arrPlace" : r["routes"][1]["arrPlace"],
    "route_1_depPlace" : r["routes"][1]["depPlace"],
    "route_1_distance" : r["routes"][1]["distance"],
    "route_1_totalDuration" : r["routes"][1]["totalDuration"],
    "route_1_url" : r["routes"][1]["segments"][0]["agencies"][0]["links"][0]["url"],
    "route_2_name" : r["routes"][2]["name"],
    "route_2_arrPlace" : r["routes"][2]["arrPlace"],
    "route_2_depPlace" : r["routes"][2]["depPlace"],
    "route_2_distance" : r["routes"][2]["distance"],
    "route_2_totalDuration" : r["routes"][2]["totalDuration"],
    "route_2_url" : r["routes"][2]["segments"][0]["agencies"][0]["links"][0]["url"],
    "route_3_name" : r["routes"][3]["name"],
    "route_3_arrPlace" : r["routes"][3]["arrPlace"],
    "route_3_depPlace" : r["routes"][3]["depPlace"],
    "route_3_distance" : r["routes"][3]["distance"],
    "route_3_totalDuration" : r["routes"][3]["totalDuration"],
    "route_3_url" : r["routes"][3]["segments"][0]["agencies"][0]["links"][0]["url"],
    }

    str1 = str(R2R_categories)
    str2 = str(zomatoRestaurants)
    str_emailContent = str1 + str2
    content_function = content_string(str_emailContent)

    return render_template("results.html", R2R_categories=R2R_categories, zomatoRestaurants=zomatoRestaurants)

@app.route("/email_content", methods=["POST"])
def content_string(str_emailContent):
    print str_emailContent
    return 1

@app.route("/email", methods=["POST"])
def email_address():
    email_recipient = request.form["email"]
    email_content = "hello"
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

@app.route("/further_info")
def further_info():
    return render_template("further.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

app.run(debug=True)
