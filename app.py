from flask import Flask, render_template, Response
import os
import csv
import json

"""
Structure of the csv file, event_data array:
	Event ID: similar to event name, but without any spaces and spl characters except hyphen (-), and all lowercase
	Event Name : 50 characters max
	Description: 300 characters max
	Team size: int
	Rules and regulations: 700 char max
	Contact us: (text) Event organizers' name, phone number, mail ID
"""

event_data = {}

# read the file and save the data in mem when application is deployed.
with open('event_data.csv', newline='') as file:
	rows = csv.reader(file, dialect='excel')
	next(rows) # skips the first entry which has headings
	for row in rows:
		event_data[row[0]] = {"name": row[1], "description": row[2], "team-size": int(row[3]), "rules": row[4], "contact": row[5]}

app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/events')
def events_main():
	return render_template('events.html')

@app.route('/events/<event_name>')
def event_particular(event_name):
	data = json.dumps(event_data[event_name])
	return Response(data, mimetype='application/json')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)