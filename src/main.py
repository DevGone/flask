from flask import Flask, render_template, request, jsonify
from raspberric import get_history
import urllib2
app = Flask(__name__)

@app.route("/")
def root():
	req = urllib2.Request("http://devgone.herokuapp.com/measures/")
	req.data = jsonify(status="prout").data
	req.get_method = lambda: "POST"
	response = urllib2.urlopen(req)
	data = response.read()
	return "Yo bitch !" + str(data)

#field : papp
#step : step in seconds to get data
#duration_type : week, day, hour, minute, second
#duration : value in fonction of the duration_type
@app.route("/gethistory", methods=['GET'])
def gethistory():
	return get_history(request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

if __name__ == "__main__":
	app.debug = True
	app.run()
