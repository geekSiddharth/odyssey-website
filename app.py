from flask import Flask, render_template, abort
import os
import csv

"""
Structure of the csv file, event_data array:
	Event ID: similar to event name, but without any spaces and spl characters except hyphen (-), and all lowercase
	Event Name : 50 characters max
	Description: 300 characters max
	Team size: int
	Rules and regulations: 700 char max
	Contact us: (text) Event organizers' name, phone number, mail ID
	Entry Fee
	FB Event Link
"""

event_data = {}

# read the file and save the data in mem when application is deployed.
with open('event_data.csv', newline='') as file:
	rows = csv.reader(file, dialect='excel')
	next(rows) # skips the first entry which has headings
	for row in rows:
		event_data[row[0]] = {"name": row[1], "description": row[2], "teamSize": int(row[3]), "rules": row[4], "contact": row[5], "entryFee": int(row[6]), "fbEventLink": row[7]}
	file.close()

app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/events')
def events():
	return render_template('events.html')

# @app.route('/register')
# def register():
# 	return render_template('register.html')

@app.route('/events/<event_name>')
def event_particular(event_name):
	if event_name in event_data:
		data = event_data[event_name]
		return render_template('event-modal.html', event = data)
	else:
		abort(404)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)