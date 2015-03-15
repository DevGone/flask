
from flask import Flask, render_template, request
from raspberric import get_history, polling

app = Flask(__name__)

@app.route("/")
def root():
	return "Yo bitch !"

@app.route("/getdata/")
@app.route("/getdata/<name>")
def test(name=None):
	return render_template('hello.html', name=name, data=getData())

#field : papp
#step : step in seconds to get data
#duration_type : week, day, hour, minute, second
#duration : value in fonction of the duration_type
@app.route("/gethistory", methods=['GET'])
def gethistory():
	return get_history(request.args.get('field'), request.args.get('step'), request.args.get('duration_type'), request.args.get('duration'))

def bgr():
	print "coucou"

if __name__ == "__main__":
	polling(5, bgr)
	app.debug = True
	app.run()
