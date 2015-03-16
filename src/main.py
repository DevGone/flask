from flask import Flask, render_template
from raspberric import get_history
from distant import startPollingRaspberric

app = Flask(__name__)

@app.route("/")
def root():
	return "Hello"

#field : papp
#step : step in seconds to get data
#duration_type : week, day, hour, minute, second
#duration : value in fonction of the duration_type
@app.route("/gethistory", methods=['GET'])
def gethistory():
	return get_history(request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

if __name__ == "__main__":
	startPollingRaspberric(60)
	app.run()
