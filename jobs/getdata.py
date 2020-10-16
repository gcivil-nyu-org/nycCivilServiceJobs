import requests
import json
import pandas as pd
from sodapy import Socrata
import csv


'''def getjob_data(restaurant_name, restaurant_location):
    location_list = restaurant_location.split(", ")
    address1 = location_list[0]
    city = location_list[1]
    state = location_list[2]
    country = 'US'

    api_key = 'JaekzvTTKsWGtQ96HUiwAXOUwRt6Ndbqzch4zc2XFnOEBxwTmwr-esm1uWo2QFvFJtXS8nY2dXx51cfAnMqVHpHRcp8N7QtP7LNVCcoxJWV_9NJrmZWSMiq-R_mEX3Yx'
    headers = {'Authorization': 'Bearer %s' % api_key}
    url = 'https://api.yelp.com/v3/businesses/matches'
    params = {'name': restaurant_name, 'address1': address1, 'city': city, 'state': state, 'country': country}

    response = requests.get(url, params=params, headers=headers)
    return response.text.encode("utf8")
'''

def getJobs():
    client = Socrata("data.cityofnewyork.us",
                     "m7QHRP2U6tqRR7XCge8TzIRUW",
                     username="nycCivilService.csgy6063@gmail.com",
                     password="team4Pythonpir@tes")
    results = client.get("kpav-sd4t", limit=100)

    return results        
