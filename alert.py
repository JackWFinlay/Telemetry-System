#!/usr/bin/python

# Author: Jack Finlay
# This file sends the alerts to OpsGenie.

import json
import urllib2
import sys
import time

with open("alertConfig.json") as config:
    data = json.load(config)

requestBody = {
        "apiKey": data["apiKey"],
        "message": data["message"],
        "recipients": data["recipients"],
        "user": data["user"] 
}

req = urllib2.Request('https://api.opsgenie.com/v1/json/alert') # Generates the request URL.
req.add_header('Content-Type', 'application/json') # Sets header to JSON type.

response = urllib2.urlopen(req, json.dumps(requestBody)) # Gets the response from the API.

responsejson = json.load(response) # Parse JSON Response.

# OpsGenie does not currently appear to be alerting to recipients properly, so we have to assign the alert manually.
if (str(responsejson["status"]) == "successful" and int(responsejson["code"]) == 200 ): # If alert sent okay, assign it to the specified person.
	
	assignRequestBody = {
		"apiKey": data["apiKey"],
		"id": responsejson["alertId"],
		"owner": data["user"]
	}

	assignReq = urllib2.Request('https://api.opsgenie.com/v1/json/alert/assign')
	assignReq.add_header('Content-Type', 'application/json')

	assignResponse = urllib2.urlopen(assignReq, json.dumps(assignRequestBody))

exit(0)