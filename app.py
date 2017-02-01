from flask import Flask, render_template, abort, request
import os
import csv
import requests
import registration
import json
from data import config, event_data, event_form

app = Flask('__name__')
app.config['SECRET_KEY']=os.urandom(20)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/events/')
def events():
	return render_template('events.html')

@app.route('/register/<event_id>', methods=['GET', 'POST'])
def register(event_id):
	if event_id in event_data:
		if request.method == 'POST':
			recaptcha_result = requests.post("https://www.google.com/recaptcha/api/siteverify", data={"secret":config["recaptcha-secret"], "response":request.form["g-recaptcha-response"], "remoteip": request.remote_addr})
			if recaptcha_result.json()["success"] or config["developement"]:
				processed_data = registration.process_post_request(request.form, event_id)
				registration.insert_record(processed_data, event_id)
			else:
				render_template('register_response.html', error="Wrong Catpcha")
		return render_template('register.html', event=event_form[event_id])
	else:
		abort(404)

@app.route('/events/<event_id>')
def event_particular(event_id):
	if event_id in event_data:
		data = event_data[event_id]
		return render_template('event-modal.html', event = data)
	else:
		abort(404)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)
