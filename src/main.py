from flask import Flask, render_template
from raspberric import get_history_from_now
import urllib2, requests
app = Flask(__name__)

@app.route("/")
def root():
	json = get_history_from_now("papp", 60*60, 'hour', 24)
	req = requests.post("http://devgone.herokuapp.com/measures/", data=json)
	return req.text

#field : papp
#step : step in seconds to get data
#duration_type : week, day, hour, minute, second
#duration : value in fonction of the duration_type
@app.route("/gethistoryfromnow", methods=['GET'])
def gethistory():
	return get_history_from_now(request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

if __name__ == "__main__":
	app.debug = True
	app.run()
