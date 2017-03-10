import json
import csv
from gfm import gfm, markdown
from collections import OrderedDict
import html2text

h = html2text.HTML2Text()
h.ignore_links = True

def html2md(html):
	return h.handle(html)

with open('sensitive_data.json', newline='') as file:
    global config
    config = json.loads(file.read())

"""
(obsolete now)
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
			"textName": html2md(row[1]).replace('"', '&quot;'),
			"description": markdown(gfm(row[2])), 
			"textDescription": html2md(markdown(gfm(row[2]))).replace('"', '&quot;'),
			"teamSize": row[3], 
			"teamSizeMax": row[4],
			"rules": markdown(gfm(row[5])), 
			"contact": markdown(gfm(row[6])), 
			"entryFee": row[7], 
			"fbEventLink": row[8],
			"categories": row[9],
			"formLink": row[10]
		}

	file.close()