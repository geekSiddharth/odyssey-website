import json
import csv
from gfm import gfm, markdown
from collections import OrderedDict

with open('sensitive_data.json', newline='') as file:
    global config
    config = json.loads(file.read())

"""
Structure of the csv file, event_data array:
	Event ID: similar to event name, but without any spaces and spl characters except hyphen (-), and all lowercase
	Event Name : 50 characters max
	Description: 300 characters max
	Team size: int
	Rules and regulations: 700 char max
	Contact us: (text) Event organizers' name, phone number, mail ID
	Entry Fe
	FB Event Link
"""

event_data = {}

# read the file and save the data in mem when application is deployed.
with open('event_data.csv', newline='', encoding='utf8') as file:
	rows = csv.reader(file, dialect='excel')
	next(rows) # skips the first entry which has headings
	for row in rows:
		event_data[row[0]] = {
			"event-id":row[0],
			"name": row[1], 
			"description": markdown(gfm(row[2])), 
			"teamSize": row[3], 
			"rules": markdown(gfm(row[4])), 
			"contact": markdown(gfm(row[5])), 
			"entryFee": row[6], 
			"fbEventLink": row[7],
			"categories": row[8]
		}

		try:
			event_data[row[0]]["teamSizeMin"] = int(row[3].split("-")[0]) 
			event_data[row[0]]["teamSizeMax"] = int(row[3].split("-")[-1]) # max and min will be the same if there's no dash
			event_data[row[0]]["onlyBatmanAndRobin"] = event_data[row[0]]["teamSizeMax"] > 4
		except:
			event_data[row[0]]["onlyBatmanAndRobin"] = True
			print("Warning, team size for %s is %s" % (row[0], row[3]))

	file.close()


with open('event_forms.json', newline='') as file:
    global event_form
    event_form = {}
    event_form_raw = json.loads(file.read(),  object_pairs_hook=OrderedDict)
    for k in event_form_raw:
        event = dict(event_data[k])
        event["data"] = event_form_raw[k]
        event_form[k] = event


sth = {
	"a-cappella": {
	    "captain": {
	        "name": "Participant A",
	        "email": "pa",
	        "phone_number": "pam",
	        "institute": "lel"
	    },
	    "other_participants": [
	        {
	            "name": "Participant B",
	            "email": "pb",
	            "phone_number": "pbm",
	            "institute": "lel"
	         },
	    ],
	    "team_name": "ha",
	    "team_size": 2,
	    "data": {
	        "some": "json"
	    }
	}
}
