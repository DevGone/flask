from flask import Flask, render_template, request
from distant import startPollingRaspberric, startHerokuIdlingPrevention
from raspberric import get_history_from_now, get_consumption_from_now
import requests

app = Flask(__name__)

@app.route("/")
def root():
	return "Hello"

#field : papp
#step : step in seconds to get data
#duration_type : week, day, hour, minute, second
#duration : value in fonction of the duration_type
@app.route("/gethistoryfromnow", methods=['GET'])
def gethistory():
	return get_history_from_now(request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

@app.route("/getconsumptionfromnow", methods=['GET'])
def getconsumptionfromnow():
	return get_consumption_from_now(request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

if __name__ == "__main__":
	startPollingRaspberric(60)
	startHerokuIdlingPrevention()
	app.debug = True
	app.run()
