from flask import Flask, render_template, abort, request, redirect
import os
import csv
import requests
#import registration
import json
from data import config, event_data #, event_form

app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/events/')
def events():
	return render_template('events.html', events=event_data)

@app.route('/contact/')
def contact():
	return render_template('contact.html')

@app.route('/bobby/')
def bobby():
	return render_template('bobby-workshop.html')

@app.route('/college-trophy/')
def college_trophy():
	return render_template('college-trophy.html')

@app.route('/accommodation/')
def accommodation():
	return render_template('accomodation.html')

@app.route('/register/<event_id>', methods=['GET', 'POST'])
def register(event_id):
	if event_id in event_data:
		data = event_data[event_id]
		return redirect(data["formLink"])
	else:
		abort(404)

@app.route('/events/<event_id>')
def event_particular(event_id):
	if event_id=="design-360":
		return render_template('design360.html')
	if event_id in event_data:
		data = event_data[event_id]
		return render_template('event-modal.html', event = data)
	else:
		abort(404)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=int(config["site-port"]),debug=True)
