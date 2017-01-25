from flask import Flask, render_template
import os

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
#
# @app.route('/event-modal')
# def event_modal():
# 	return render_template('event-modal.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8000,debug=True)