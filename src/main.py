from flask import Flask, render_template, request
from distant import startPollingRaspberric, startHerokuIdlingPrevention
from raspberric import get_history_from_now, get_consumption_from_now, get_yesterday_consumption, get_informations, get_last_hour_consumption
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
	return get_history_from_now(request.args.get('raspberricId'), request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

@app.route("/getconsumptionfromnow", methods=['GET'])
def getconsumptionfromnow():
	return get_consumption_from_now(request.args.get('raspberricId'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

@app.route("/getyesterdayconsumption", methods=['GET'])
def getyesterdayconsumption():
	return get_yesterday_consumption('vf6sxo78')

@app.route("/getlasthourconsumption", methods=['GET'])
def getlasthourconsumption():
	return get_last_hour_consumption('vf6sxo78')

@app.route("/getinformations", methods=['GET'])
def getinformations():
	return get_informations('vf6sxo78')

if __name__ == "__main__":
	raspberricIds = ['vf6sxo78']
	startPollingRaspberric(3600, raspberricIds)
	startHerokuIdlingPrevention()
	app.run()
