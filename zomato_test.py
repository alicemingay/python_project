import requests

# --- Rome to Rio API.
#R2R_API = "QQidc5EJ"

#def getRoute():
#    endpoint = "http://free.rome2rio.com/api/1.4/json/Search"
#    payload = {"key": R2R_API, "oName": "London", "dName": "Paris"}
#    r = requests.get(endpoint, params=payload).json()

#    r2r_long_lat = {

#    	latitude : r["places"][1]["_lat"],
#    	longitude : r["places"][1]["_lng"]

#    }

#    print r2r_long_lat

#getRoute()

# --- Zomato API. 
def get_restaurants(latitude, longitude):
    endpoint = "https://developers.zomato.com/api/v2.1/geocode?"
    headers = {"Accept": "application/json", "user-key": "429234119628421c785014cda06c4308"}
    params = {"lat": latitude, "lon": longitude}
    req = requests.get(endpoint, headers=headers, params=params).json()

    print req

get_restaurants(48.85334, 2.34604)

#curl -X GET --header "Accept: application/json" --header "user-key: 429234119628421c785014cda06c4308" "https://developers.zomato.com/api/v2.1/geocode?lat=40.732013&lon=-73.996155"

# --- Issues faced: 
# 1) Zomato API doesn't seem to accept LONG and LAT co-ordinates from countries outside of 
# UK and US. Not sure how to work around this or what is going on. 
# 2) How do we connect the co-ords given from the R2R API and pass them into
# Zomato as parameters? 
