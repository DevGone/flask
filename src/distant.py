import threading, requests
from raspberric import get_history

def polling(timeInterval, callback):
	thread = threading.Timer(timeInterval, lambda: polling(timeInterval, callback))
	thread.daemon = True
	callback()

def fetchRaspberricData():
	json = get_history("papp", 60*60, 'hour', 24)
	return json

def sendData(data, url="http://devgone.herokuapp.com/measures/"):
	return requests.post(url, data=data).text

def repeatTask():
	#json = fetchRaspberricData()
	#print sendData(json)
	print 'ok'

def startPollingRaspberric(timeInterval):
	polling(timeInterval, repeatTask)
